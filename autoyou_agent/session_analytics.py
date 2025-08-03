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

"""Session analytics utilities for autoyou_agent.

This module provides functions to analyze user interactions and agent responses
stored in the TinyDB session service.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
from tinydb import Query

from tinydb_session_service import TinyDBSessionService


class SessionAnalytics:
    """Analytics class for session data analysis."""
    
    def __init__(self, session_service: TinyDBSessionService):
        self.session_service = session_service
    
    def get_user_session_summary(self, app_name: str, user_id: str) -> Dict[str, Any]:
        """Get a comprehensive summary of all sessions for a user."""
        session_query = Query()
        sessions = self.session_service.sessions_table.search(
            (session_query.app_name == app_name) & (session_query.user_id == user_id)
        )
        
        interaction_query = Query()
        all_interactions = self.session_service.agent_interactions_table.search(
            (interaction_query.app_name == app_name) & (interaction_query.user_id == user_id)
        )
        
        # Calculate summary statistics
        total_sessions = len(sessions)
        total_interactions = len(all_interactions)
        user_questions = len([i for i in all_interactions if i['is_user_question']])
        agent_responses = len([i for i in all_interactions if i['is_agent_response']])
        agent_transfers = len([i for i in all_interactions if i['is_transfer_to_agent']])
        
        # Most used agents
        agent_usage = Counter([i['agent_name'] for i in all_interactions if i['agent_name']])
        
        # Session activity over time
        session_dates = [datetime.fromisoformat(s['created_at'].replace('Z', '+00:00')).date() 
                        for s in sessions]
        daily_activity = Counter(session_dates)
        
        return {
            'user_id': user_id,
            'app_name': app_name,
            'total_sessions': total_sessions,
            'total_interactions': total_interactions,
            'user_questions': user_questions,
            'agent_responses': agent_responses,
            'agent_transfers': agent_transfers,
            'most_used_agents': dict(agent_usage.most_common(10)),
            'daily_activity': {str(date): count for date, count in daily_activity.items()},
            'sessions': [
                {
                    'session_id': s['id'],
                    'created_at': s['created_at'],
                    'updated_at': s['updated_at']
                }
                for s in sorted(sessions, key=lambda x: x['created_at'], reverse=True)
            ]
        }
    
    def get_agent_usage_statistics(self, app_name: str, days: int = 30) -> Dict[str, Any]:
        """Get statistics on agent usage across all users."""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        interaction_query = Query()
        recent_interactions = [
            i for i in self.session_service.agent_interactions_table.search(
                interaction_query.app_name == app_name
            )
            if datetime.fromisoformat(i['created_at'].replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Agent transfer statistics
        transfers = [i for i in recent_interactions if i['is_transfer_to_agent']]
        agent_transfers = Counter([t['agent_name'] for t in transfers if t['agent_name']])
        
        # User engagement by agent
        agent_users = defaultdict(set)
        for interaction in recent_interactions:
            if interaction['agent_name']:
                agent_users[interaction['agent_name']].add(interaction['user_id'])
        
        agent_user_counts = {agent: len(users) for agent, users in agent_users.items()}
        
        # Daily transfer patterns
        daily_transfers = defaultdict(int)
        for transfer in transfers:
            date = datetime.fromisoformat(transfer['created_at'].replace('Z', '+00:00')).date()
            daily_transfers[str(date)] += 1
        
        return {
            'app_name': app_name,
            'analysis_period_days': days,
            'total_interactions': len(recent_interactions),
            'total_transfers': len(transfers),
            'agent_transfer_counts': dict(agent_transfers),
            'agent_user_counts': agent_user_counts,
            'daily_transfer_activity': dict(daily_transfers),
            'most_popular_agents': dict(agent_transfers.most_common(10))
        }
    
    def detect_conversation_patterns(self, app_name: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """Detect patterns in a specific conversation session."""
        interaction_query = Query()
        interactions = self.session_service.agent_interactions_table.search(
            (interaction_query.app_name == app_name) & 
            (interaction_query.user_id == user_id) & 
            (interaction_query.session_id == session_id)
        )
        
        # Sort by timestamp
        interactions.sort(key=lambda x: x['timestamp'])
        
        # Detect transfer loops
        transfer_sequence = []
        for interaction in interactions:
            if interaction['is_transfer_to_agent'] and interaction['agent_name']:
                transfer_sequence.append(interaction['agent_name'])
        
        # Find loops in transfer sequence
        loops = self._find_loops_in_sequence(transfer_sequence)
        
        # Calculate response times (simplified)
        question_response_pairs = []
        current_question = None
        for interaction in interactions:
            if interaction['is_user_question']:
                current_question = interaction
            elif interaction['is_agent_response'] and current_question:
                response_time = interaction['timestamp'] - current_question['timestamp']
                question_response_pairs.append({
                    'question_time': current_question['timestamp'],
                    'response_time': interaction['timestamp'],
                    'duration_seconds': response_time,
                    'question_summary': current_question['content_summary'],
                    'response_summary': interaction['content_summary']
                })
                current_question = None
        
        return {
            'session_id': session_id,
            'total_interactions': len(interactions),
            'transfer_sequence': transfer_sequence,
            'detected_loops': loops,
            'question_response_pairs': question_response_pairs,
            'agents_involved': list(set([i['agent_name'] for i in interactions if i['agent_name']])),
            'conversation_duration': (
                interactions[-1]['timestamp'] - interactions[0]['timestamp']
                if len(interactions) > 1 else 0
            )
        }
    
    def _find_loops_in_sequence(self, sequence: List[str]) -> List[Dict[str, Any]]:
        """Find loops in a sequence of agent transfers."""
        loops = []
        
        for i in range(len(sequence)):
            for j in range(i + 2, len(sequence) + 1):
                subsequence = sequence[i:j]
                if len(subsequence) >= 3:  # Minimum loop size
                    # Check if this subsequence repeats
                    pattern_length = len(subsequence)
                    for k in range(j, len(sequence)):
                        if k + pattern_length <= len(sequence):
                            next_subsequence = sequence[k:k + pattern_length]
                            if subsequence == next_subsequence:
                                loops.append({
                                    'pattern': subsequence,
                                    'start_index': i,
                                    'end_index': k + pattern_length - 1,
                                    'repetitions': 2,
                                    'pattern_length': pattern_length
                                })
                                break
        
        return loops
    
    def get_frequent_user_questions(self, app_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most frequent user questions across all sessions."""
        interaction_query = Query()
        user_questions = self.session_service.agent_interactions_table.search(
            (interaction_query.app_name == app_name) & 
            (interaction_query.is_user_question == True)
        )
        
        # Group similar questions (simplified by first 100 characters)
        question_groups = defaultdict(list)
        for question in user_questions:
            if question['content_summary']:
                key = question['content_summary'][:100].lower().strip()
                question_groups[key].append(question)
        
        # Sort by frequency
        frequent_questions = [
            {
                'question_pattern': key,
                'frequency': len(questions),
                'example_full_question': questions[0]['content_summary'],
                'users_asked': len(set([q['user_id'] for q in questions])),
                'recent_timestamp': max([q['timestamp'] for q in questions])
            }
            for key, questions in question_groups.items()
        ]
        
        frequent_questions.sort(key=lambda x: x['frequency'], reverse=True)
        return frequent_questions[:limit]
    
    def export_session_data(self, app_name: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """Export all data for a specific session for analysis or debugging."""
        # Get session info
        session_query = Query()
        session = self.session_service.sessions_table.get(
            (session_query.app_name == app_name) & 
            (session_query.user_id == user_id) & 
            (session_query.id == session_id)
        )
        
        # Get all events
        event_query = Query()
        events = self.session_service.events_table.search(
            (event_query.app_name == app_name) & 
            (event_query.user_id == user_id) & 
            (event_query.session_id == session_id)
        )
        
        # Get all interactions
        interaction_query = Query()
        interactions = self.session_service.agent_interactions_table.search(
            (interaction_query.app_name == app_name) & 
            (interaction_query.user_id == user_id) & 
            (interaction_query.session_id == session_id)
        )
        
        return {
            'session': session,
            'events': sorted(events, key=lambda x: x['timestamp']),
            'interactions': sorted(interactions, key=lambda x: x['timestamp']),
            'summary': self.session_service.get_agent_interaction_summary(app_name, user_id, session_id)
        }


def create_analytics_instance(db_path: str = "autoyou_sessions.json") -> SessionAnalytics:
    """Create a SessionAnalytics instance with a TinyDB session service."""
    session_service = TinyDBSessionService(db_path)
    return SessionAnalytics(session_service)