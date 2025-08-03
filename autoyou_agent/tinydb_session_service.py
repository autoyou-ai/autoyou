# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from google.adk.sessions.base_session_service import BaseSessionService, GetSessionConfig, ListSessionsResponse
from google.adk.sessions.session import Session
from google.adk.sessions.state import State
from google.adk.events.event import Event

logger = logging.getLogger("autoyou_agent." + __name__)


class TinyDBSessionService(BaseSessionService):
    """A session service that uses TinyDB for storage.
    
    This service tracks user questions and agent responses across all sub-agents
    in the autoyou_agent system.
    """

    def __init__(self, db_path: str = "autoyou_sessions.json"):
        """Initialize the TinyDB session service.
        
        Args:
            db_path: Path to the TinyDB JSON file for storing sessions.
        """
        self.db = TinyDB(db_path, storage=CachingMiddleware(JSONStorage))
        
        # Create separate tables for different data types
        self.sessions_table = self.db.table('sessions')
        self.events_table = self.db.table('events')
        self.app_state_table = self.db.table('app_state')
        self.user_state_table = self.db.table('user_state')
        self.agent_interactions_table = self.db.table('agent_interactions')
        
        logger.info(f"TinyDB session service initialized with database: {db_path}")
    
    def close(self):
        """Close the database and ensure all data is flushed."""
        self.db.close()
        logger.info("TinyDB session service closed")
    
    def flush(self):
        """Flush any pending writes to disk."""
        # Force a write by accessing the storage
        self.db.storage.flush()
        logger.debug("TinyDB session service flushed")

    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        state: Optional[dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Session:
        """Create a new session."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if state is None:
            state = {}
        
        # Extract state components
        app_state_delta, user_state_delta, session_state = self._extract_state_delta(state)
        
        # Get or create app state
        app_query = Query()
        app_state_doc = self.app_state_table.get(app_query.app_name == app_name)
        if app_state_doc:
            app_state = app_state_doc['state']
            app_state.update(app_state_delta)
            self.app_state_table.update({'state': app_state}, app_query.app_name == app_name)
        else:
            app_state = app_state_delta
            self.app_state_table.insert({
                'app_name': app_name,
                'state': app_state,
                'created_at': datetime.now(timezone.utc).isoformat()
            })
        
        # Get or create user state
        user_query = Query()
        user_state_doc = self.user_state_table.get(
            (user_query.app_name == app_name) & (user_query.user_id == user_id)
        )
        if user_state_doc:
            user_state = user_state_doc['state']
            user_state.update(user_state_delta)
            self.user_state_table.update(
                {'state': user_state}, 
                (user_query.app_name == app_name) & (user_query.user_id == user_id)
            )
        else:
            user_state = user_state_delta
            self.user_state_table.insert({
                'app_name': app_name,
                'user_id': user_id,
                'state': user_state,
                'created_at': datetime.now(timezone.utc).isoformat()
            })
        
        # Merge states
        merged_state = self._merge_state(app_state, user_state, session_state)
        
        # Create session record
        session_doc = {
            'app_name': app_name,
            'user_id': user_id,
            'id': session_id,
            'state': session_state,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        self.sessions_table.insert(session_doc)
        
        # Create session object
        session = Session(
            app_name=app_name,
            user_id=user_id,
            id=session_id,
            state=merged_state,
            events=[],
            last_update_time=datetime.now(timezone.utc).timestamp()
        )
        
        logger.info(f"Created session {session_id} for user {user_id} in app {app_name}")
        return session

    async def get_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: Optional[GetSessionConfig] = None,
    ) -> Optional[Session]:
        """Get an existing session."""
        session_query = Query()
        session_doc = self.sessions_table.get(
            (session_query.app_name == app_name) & 
            (session_query.user_id == user_id) & 
            (session_query.id == session_id)
        )
        
        if not session_doc:
            return None
        
        # Get events for this session
        event_query = Query()
        event_filter = (
            (event_query.app_name == app_name) & 
            (event_query.user_id == user_id) & 
            (event_query.session_id == session_id)
        )
        
        if config and config.after_timestamp:
            after_dt = datetime.fromtimestamp(config.after_timestamp)
            event_docs = [
                doc for doc in self.events_table.search(event_filter)
                if datetime.fromisoformat(doc['timestamp'].replace('Z', '+00:00')) >= after_dt
            ]
        else:
            event_docs = self.events_table.search(event_filter)
        
        # Sort by timestamp and limit if needed
        event_docs.sort(key=lambda x: x['timestamp'], reverse=True)
        if config and config.num_recent_events:
            event_docs = event_docs[:config.num_recent_events]
        
        # Convert to Event objects
        events = [self._doc_to_event(doc) for doc in reversed(event_docs)]
        
        # Get states
        app_state = self._get_app_state(app_name)
        user_state = self._get_user_state(app_name, user_id)
        session_state = session_doc['state']
        
        # Merge states
        merged_state = self._merge_state(app_state, user_state, session_state)
        
        # Create session object
        session = Session(
            app_name=app_name,
            user_id=user_id,
            id=session_id,
            state=merged_state,
            events=events,
            last_update_time=datetime.fromisoformat(session_doc['updated_at'].replace('Z', '+00:00')).timestamp()
        )
        
        return session

    async def list_sessions(self, *, app_name: str, user_id: str) -> ListSessionsResponse:
        """List all sessions for a user in an app."""
        session_query = Query()
        session_docs = self.sessions_table.search(
            (session_query.app_name == app_name) & (session_query.user_id == user_id)
        )
        
        sessions = []
        for doc in session_docs:
            session = Session(
                app_name=doc['app_name'],
                user_id=doc['user_id'],
                id=doc['id'],
                state=doc['state'],
                events=[],  # Events not included in list response
                last_update_time=datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00')).timestamp()
            )
            sessions.append(session)
        
        return ListSessionsResponse(sessions=sessions)

    async def delete_session(self, app_name: str, user_id: str, session_id: str) -> None:
        """Delete a session and all its events."""
        session_query = Query()
        event_query = Query()
        
        # Delete session
        self.sessions_table.remove(
            (session_query.app_name == app_name) & 
            (session_query.user_id == user_id) & 
            (session_query.id == session_id)
        )
        
        # Delete associated events
        self.events_table.remove(
            (event_query.app_name == app_name) & 
            (event_query.user_id == user_id) & 
            (event_query.session_id == session_id)
        )
        
        # Delete associated agent interactions
        interaction_query = Query()
        self.agent_interactions_table.remove(
            (interaction_query.app_name == app_name) & 
            (interaction_query.user_id == user_id) & 
            (interaction_query.session_id == session_id)
        )
        
        logger.info(f"Deleted session {session_id} for user {user_id} in app {app_name}")

    async def append_event(self, session: Session, event: Event) -> Event:
        """Append an event to a session and track agent interactions."""
        # Store the event
        event_doc = self._event_to_doc(session, event)
        self.events_table.insert(event_doc)
        
        # Track agent interactions for user questions and agent responses
        self._track_agent_interaction(session, event)
        
        # Update session state if needed
        if event.actions and event.actions.state_delta:
            app_state_delta, user_state_delta, session_state_delta = self._extract_state_delta(
                event.actions.state_delta
            )
            
            # Update states
            if app_state_delta:
                self._update_app_state(session.app_name, app_state_delta)
            if user_state_delta:
                self._update_user_state(session.app_name, session.user_id, user_state_delta)
            if session_state_delta:
                self._update_session_state(session.app_name, session.user_id, session.id, session_state_delta)
        
        # Update session timestamp
        session_query = Query()
        self.sessions_table.update(
            {'updated_at': datetime.now(timezone.utc).isoformat()},
            (session_query.app_name == session.app_name) & 
            (session_query.user_id == session.user_id) & 
            (session_query.id == session.id)
        )
        
        # Call parent method to update in-memory session
        await super().append_event(session=session, event=event)
        
        logger.debug(f"Appended event {event.id} to session {session.id}")
        return event

    def _track_agent_interaction(self, session: Session, event: Event) -> None:
        """Track agent interactions for analytics and debugging."""
        interaction_doc = {
            'app_name': session.app_name,
            'user_id': session.user_id,
            'session_id': session.id,
            'event_id': event.id,
            'author': event.author,
            'timestamp': event.timestamp,
            'content_type': None,
            'content_summary': None,
            'agent_name': None,
            'is_user_question': False,
            'is_agent_response': False,
            'is_transfer_to_agent': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Analyze event content
        if event.content:
            content_dict = event.content.model_dump() if hasattr(event.content, 'model_dump') else event.content
            
            # Check if it's a user question
            if event.author == 'user':
                interaction_doc['is_user_question'] = True
                interaction_doc['content_type'] = 'user_input'
                if isinstance(content_dict, dict) and 'parts' in content_dict:
                    parts = content_dict['parts']
                    if parts and isinstance(parts[0], dict) and 'text' in parts[0]:
                        text_content = parts[0]['text'][:200]  # First 200 chars
                        interaction_doc['content_summary'] = text_content
            
            # Check if it's an agent response
            elif event.author == 'model':
                interaction_doc['is_agent_response'] = True
                interaction_doc['content_type'] = 'agent_response'
                if isinstance(content_dict, dict) and 'parts' in content_dict:
                    parts = content_dict['parts']
                    if parts and isinstance(parts[0], dict) and 'text' in parts[0]:
                        text_content = parts[0]['text'][:200]  # First 200 chars
                        interaction_doc['content_summary'] = text_content
        
        # Check for transfer_to_agent actions
        if event.actions:
            actions_dict = event.actions.model_dump() if hasattr(event.actions, 'model_dump') else event.actions
            if isinstance(actions_dict, dict) and 'function_calls' in actions_dict:
                function_calls = actions_dict['function_calls']
                for call in function_calls:
                    if isinstance(call, dict) and call.get('name') == 'transfer_to_agent':
                        interaction_doc['is_transfer_to_agent'] = True
                        if 'args' in call and 'agent_name' in call['args']:
                            interaction_doc['agent_name'] = call['args']['agent_name']
                        break
        
        self.agent_interactions_table.insert(interaction_doc)

    def get_agent_interaction_summary(self, app_name: str, user_id: str, session_id: str) -> dict:
        """Get a summary of agent interactions for a session."""
        interaction_query = Query()
        interactions = self.agent_interactions_table.search(
            (interaction_query.app_name == app_name) & 
            (interaction_query.user_id == user_id) & 
            (interaction_query.session_id == session_id)
        )
        
        summary = {
            'total_interactions': len(interactions),
            'user_questions': len([i for i in interactions if i['is_user_question']]),
            'agent_responses': len([i for i in interactions if i['is_agent_response']]),
            'agent_transfers': len([i for i in interactions if i['is_transfer_to_agent']]),
            'agents_used': list(set([i['agent_name'] for i in interactions if i['agent_name']])),
            'interaction_timeline': [
                {
                    'timestamp': i['timestamp'],
                    'author': i['author'],
                    'type': i['content_type'],
                    'summary': i['content_summary'],
                    'agent_name': i['agent_name']
                }
                for i in sorted(interactions, key=lambda x: x['timestamp'])
            ]
        }
        
        return summary

    def _extract_state_delta(self, state: dict[str, Any]) -> tuple[dict, dict, dict]:
        """Extract state delta into app, user, and session components."""
        app_state_delta = {}
        user_state_delta = {}
        session_state_delta = {}
        
        for key, value in state.items():
            if key.startswith(State.APP_PREFIX):
                app_state_delta[key[len(State.APP_PREFIX):]] = value
            elif key.startswith(State.USER_PREFIX):
                user_state_delta[key[len(State.USER_PREFIX):]] = value
            else:
                session_state_delta[key] = value
        
        return app_state_delta, user_state_delta, session_state_delta

    def _merge_state(self, app_state: dict, user_state: dict, session_state: dict) -> dict:
        """Merge app, user, and session states."""
        merged_state = {}
        
        # Add app state with prefix
        for key, value in app_state.items():
            merged_state[f"{State.APP_PREFIX}{key}"] = value
        
        # Add user state with prefix
        for key, value in user_state.items():
            merged_state[f"{State.USER_PREFIX}{key}"] = value
        
        # Add session state
        merged_state.update(session_state)
        
        return merged_state

    def _get_app_state(self, app_name: str) -> dict:
        """Get app state."""
        app_query = Query()
        app_state_doc = self.app_state_table.get(app_query.app_name == app_name)
        return app_state_doc['state'] if app_state_doc else {}

    def _get_user_state(self, app_name: str, user_id: str) -> dict:
        """Get user state."""
        user_query = Query()
        user_state_doc = self.user_state_table.get(
            (user_query.app_name == app_name) & (user_query.user_id == user_id)
        )
        return user_state_doc['state'] if user_state_doc else {}

    def _update_app_state(self, app_name: str, state_delta: dict) -> None:
        """Update app state."""
        app_query = Query()
        app_state_doc = self.app_state_table.get(app_query.app_name == app_name)
        if app_state_doc:
            app_state = app_state_doc['state']
            app_state.update(state_delta)
            self.app_state_table.update({'state': app_state}, app_query.app_name == app_name)

    def _update_user_state(self, app_name: str, user_id: str, state_delta: dict) -> None:
        """Update user state."""
        user_query = Query()
        user_state_doc = self.user_state_table.get(
            (user_query.app_name == app_name) & (user_query.user_id == user_id)
        )
        if user_state_doc:
            user_state = user_state_doc['state']
            user_state.update(state_delta)
            self.user_state_table.update(
                {'state': user_state},
                (user_query.app_name == app_name) & (user_query.user_id == user_id)
            )

    def _update_session_state(self, app_name: str, user_id: str, session_id: str, state_delta: dict) -> None:
        """Update session state."""
        session_query = Query()
        session_doc = self.sessions_table.get(
            (session_query.app_name == app_name) & 
            (session_query.user_id == user_id) & 
            (session_query.id == session_id)
        )
        if session_doc:
            session_state = session_doc['state']
            session_state.update(state_delta)
            self.sessions_table.update(
                {'state': session_state},
                (session_query.app_name == app_name) & 
                (session_query.user_id == user_id) & 
                (session_query.id == session_id)
            )

    def _event_to_doc(self, session: Session, event: Event) -> dict:
        """Convert an Event to a document for storage."""
        doc = {
            'id': event.id,
            'app_name': session.app_name,
            'user_id': session.user_id,
            'session_id': session.id,
            'invocation_id': event.invocation_id,
            'author': event.author,
            'branch': event.branch,
            'timestamp': datetime.fromtimestamp(event.timestamp).isoformat(),
            'content': event.content.model_dump() if event.content and hasattr(event.content, 'model_dump') else event.content,
            'actions': event.actions.model_dump() if event.actions and hasattr(event.actions, 'model_dump') else event.actions,
            'long_running_tool_ids': event.long_running_tool_ids,
            'grounding_metadata': event.grounding_metadata.model_dump() if event.grounding_metadata and hasattr(event.grounding_metadata, 'model_dump') else event.grounding_metadata,
            'partial': event.partial,
            'turn_complete': event.turn_complete,
            'error_code': event.error_code,
            'error_message': event.error_message,
            'interrupted': event.interrupted
        }
        return doc

    def _doc_to_event(self, doc: dict) -> Event:
        """Convert a document to an Event object."""
        from google.adk.sessions import _session_util
        
        return Event(
            id=doc['id'],
            invocation_id=doc['invocation_id'],
            author=doc['author'],
            branch=doc['branch'],
            timestamp=datetime.fromisoformat(doc['timestamp']).timestamp(),
            content=_session_util.decode_content(doc['content']),
            actions=doc['actions'],
            long_running_tool_ids=doc['long_running_tool_ids'],
            grounding_metadata=_session_util.decode_grounding_metadata(doc['grounding_metadata']),
            partial=doc['partial'],
            turn_complete=doc['turn_complete'],
            error_code=doc['error_code'],
            error_message=doc['error_message'],
            interrupted=doc['interrupted']
        )

    def close(self):
        """Close the database connection."""
        self.db.close()
        logger.info("TinyDB session service closed")