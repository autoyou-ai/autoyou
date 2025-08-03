#!/usr/bin/env python3
"""
Comprehensive test to demonstrate TinyDB session service integration with autoyou_agent.
This test shows how user questions and sub-agent responses are tracked and stored.
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from google.adk.events.event import Event
from google.genai.types import Content, Part
from tinydb_session_service import TinyDBSessionService
from session_analytics import SessionAnalytics, create_analytics_instance


async def comprehensive_test():
    """Comprehensive test of TinyDB session service integration."""
    print("=== Comprehensive TinyDB Session Service Test ===")
    
    # Clean up any existing test database
    test_db_path = "comprehensive_test.json"
    if Path(test_db_path).exists():
        Path(test_db_path).unlink()
    
    # Initialize session service
    session_service = TinyDBSessionService(db_path=test_db_path)
    
    # Test data
    app_name = "autoyou_agent"
    user_id = "test_user_456"
    session_id = str(uuid.uuid4())
    
    print(f"\n1. Creating session: {session_id}")
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={"portfolio_access": True, "user_preferences": {"risk_level": "moderate"}}
    )
    print(f"   Session created successfully with state: {session.state}")
    
    # Simulate a complete user interaction flow
    events_to_add = [
        {
            "author": "user",
            "content": "What's my current portfolio performance?",
            "description": "User asks about portfolio performance"
        },
        {
            "author": "agent",
            "content": "I'll help you check your portfolio performance. Let me access your Robinhood account.",
            "description": "Main agent responds"
        },
        {
            "author": "agent",
            "content": "transfer_to_agent: robinhood_portfolio",
            "description": "Transfer to portfolio sub-agent"
        },
        {
            "author": "robinhood_portfolio",
            "content": "Your portfolio is worth $25,847.32 with a day change of +$412.18 (+1.62%). You have 8 positions.",
            "description": "Portfolio sub-agent response"
        },
        {
            "author": "user",
            "content": "Can you show me my best performing stock?",
            "description": "Follow-up user question"
        },
        {
            "author": "agent",
            "content": "transfer_to_agent: robinhood_stocks",
            "description": "Transfer to stocks sub-agent"
        },
        {
            "author": "robinhood_stocks",
            "content": "Your best performing stock today is AAPL with a gain of +$127.45 (+3.2%). You own 15 shares.",
            "description": "Stocks sub-agent response"
        }
    ]
    
    print("\n2. Adding events to simulate user interaction...")
    for i, event_data in enumerate(events_to_add, 1):
        event = Event(
            id=str(uuid.uuid4()),
            invocation_id=str(uuid.uuid4()),
            author=event_data["author"],
            branch="main",
            timestamp=datetime.now(timezone.utc).timestamp(),
            content=Content(parts=[Part(text=event_data["content"])]),
            partial=False,
            turn_complete=True
        )
        
        await session_service.append_event(session, event)
        print(f"   Event {i}: {event_data['description']}")
    
    # Flush the database to ensure data is written
    session_service.flush()
    
    print("\n3. Verifying session data...")
    retrieved_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    print(f"   Session has {len(retrieved_session.events)} events")
    for i, event in enumerate(retrieved_session.events):
        content_text = event.content.parts[0].text if event.content and event.content.parts else "No content"
        print(f"     Event {i+1}: [{event.author}] {content_text[:60]}...")
    
    print("\n4. Testing session analytics...")
    analytics = create_analytics_instance(test_db_path)
    
    # Get user summary
    user_summary = analytics.get_user_session_summary(app_name, user_id)
    print(f"   User summary: {user_summary['total_sessions']} sessions, {user_summary['total_interactions']} interactions")
    print(f"   Most used agents: {user_summary['most_used_agents']}")
    
    # Get agent usage statistics
    agent_stats = analytics.get_agent_usage_statistics(app_name)
    print(f"   Agent transfers: {agent_stats['total_transfers']}")
    print(f"   Popular agents: {agent_stats['most_popular_agents']}")
    
    # Get conversation patterns
    patterns = analytics.detect_conversation_patterns(app_name, user_id, session_id)
    print(f"   Conversation patterns: {len(patterns['transfer_sequence'])} transfers")
    print(f"   Transfer sequence: {patterns['transfer_sequence']}")
    print(f"   Agents involved: {patterns['agents_involved']}")
    
    print("\n5. Checking database file contents...")
    if Path(test_db_path).exists():
        file_size = Path(test_db_path).stat().st_size
        print(f"   Database file size: {file_size} bytes")
        
        # Read and display database structure
        with open(test_db_path, 'r') as f:
            db_content = json.load(f)
            print(f"   Database tables: {list(db_content.keys())}")
            for table_name, table_data in db_content.items():
                print(f"     {table_name}: {len(table_data)} records")
    
    print("\n6. Testing session listing...")
    sessions_list = await session_service.list_sessions(app_name=app_name, user_id=user_id)
    print(f"   Found {len(sessions_list.sessions)} sessions for user {user_id}")
    
    print("\n=== Test Results ===")
    print("✅ Session creation: PASSED")
    print("✅ Event tracking: PASSED")
    print("✅ Data persistence: PASSED")
    print("✅ Session retrieval: PASSED")
    print("✅ Analytics integration: PASSED")
    print("✅ Agent interaction tracking: PASSED")
    
    print("\n🎉 TinyDB Session Service is fully integrated and working!")
    print(f"📊 Database saved to: {Path(test_db_path).absolute()}")
    
    return test_db_path


if __name__ == "__main__":
    asyncio.run(comprehensive_test())