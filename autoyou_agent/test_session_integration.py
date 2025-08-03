#!/usr/bin/env python3
"""
Test script to verify TinyDB session service integration with autoyou_agent.
This script demonstrates how user questions and agent responses are tracked.
"""

import asyncio
import uuid
from datetime import datetime, timezone

from google.adk.events.event import Event
from google.genai.types import Content, Part
from tinydb_session_service import TinyDBSessionService
from session_analytics import SessionAnalytics, create_analytics_instance


async def test_session_tracking():
    """Test the TinyDB session service with simulated user interactions."""
    print("=== Testing TinyDB Session Service Integration ===")
    
    # Initialize session service
    session_service = TinyDBSessionService(db_path="test_sessions.json")
    
    # Create a test session
    app_name = "autoyou_agent"
    user_id = "test_user_123"
    session_id = str(uuid.uuid4())
    
    print(f"Creating session: {session_id}")
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={"initial_state": "test"}
    )
    
    # Simulate user question
    user_question_event = Event(
        id=str(uuid.uuid4()),
        invocation_id=str(uuid.uuid4()),
        author="user",
        branch="main",
        timestamp=datetime.now(timezone.utc).timestamp(),
        content=Content(parts=[Part(text="What is my portfolio balance?")]),
        partial=False,
        turn_complete=True
    )
    
    print("Adding user question event...")
    await session_service.append_event(session, user_question_event)
    
    # Simulate agent response
    agent_response_event = Event(
        id=str(uuid.uuid4()),
        invocation_id=str(uuid.uuid4()),
        author="agent",
        branch="main",
        timestamp=datetime.now(timezone.utc).timestamp(),
        content=Content(parts=[Part(text="I'll help you check your portfolio balance. Let me access your Robinhood account.")]),
        partial=False,
        turn_complete=True
    )
    
    print("Adding agent response event...")
    await session_service.append_event(session, agent_response_event)
    
    # Simulate sub-agent call (transfer_to_agent)
    subagent_call_event = Event(
        id=str(uuid.uuid4()),
        invocation_id=str(uuid.uuid4()),
        author="agent",
        branch="main",
        timestamp=datetime.now(timezone.utc).timestamp(),
        content=Content(parts=[Part(text="transfer_to_agent: robinhood_portfolio")]),
        partial=False,
        turn_complete=True
    )
    
    print("Adding sub-agent call event...")
    await session_service.append_event(session, subagent_call_event)
    
    # Simulate sub-agent response
    subagent_response_event = Event(
        id=str(uuid.uuid4()),
        invocation_id=str(uuid.uuid4()),
        author="robinhood_portfolio",
        branch="main",
        timestamp=datetime.now(timezone.utc).timestamp(),
        content=Content(parts=[Part(text="Your current portfolio balance is $15,432.67. You have 5 positions with a total day change of +$234.12 (+1.54%).")]),
        partial=False,
        turn_complete=True
    )
    
    print("Adding sub-agent response event...")
    await session_service.append_event(session, subagent_response_event)
    
    # Retrieve and verify session
    print("\nRetrieving session...")
    retrieved_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    print(f"Session has {len(retrieved_session.events)} events")
    for i, event in enumerate(retrieved_session.events):
        content_text = event.content.parts[0].text if event.content and event.content.parts else "No content"
        print(f"  Event {i+1}: {event.author} - {content_text[:50]}...")
    
    # Test analytics
    print("\n=== Testing Session Analytics ===")
    analytics = create_analytics_instance("test_sessions.json")
    
    # Get user summary
    user_summary = analytics.get_user_session_summary(app_name, user_id)
    print(f"User {user_id} has {user_summary['total_sessions']} sessions with {user_summary['total_interactions']} interactions")
    
    # Get agent usage stats
    agent_stats = analytics.get_agent_usage_statistics(app_name)
    print(f"Agent usage stats: {agent_stats}")
    
    # Get conversation patterns
    patterns = analytics.detect_conversation_patterns(app_name, user_id, session_id)
    print(f"Conversation patterns: {patterns}")
    
    print("\n=== Test Completed Successfully ===")
    print("TinyDB session service is properly integrated and tracking user interactions!")


if __name__ == "__main__":
    asyncio.run(test_session_tracking())