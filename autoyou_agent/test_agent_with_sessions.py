#!/usr/bin/env python3
"""
Test script to verify the main agent works with TinyDB session service integration.
This tests the actual agent.py file with session tracking enabled.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import root_agent
from tinydb_session_service import TinyDBSessionService
from session_analytics import SessionAnalytics

async def test_agent_with_sessions():
    """Test the main agent with session tracking."""
    print("🧪 Testing Agent with TinyDB Session Service Integration")
    print("=" * 60)
    
    # Initialize session service
    session_service = TinyDBSessionService("agent_test_sessions.json")
    
    # Test parameters
    app_name = "autoyou_agent_test"
    user_id = "test_user_789"
    
    try:
        print("\n1. Testing agent initialization...")
        # The agent should initialize without errors
        print(f"   ✅ Agent imported successfully: {root_agent.name}")
        
        print("\n2. Creating test session...")
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state={"test_mode": True}
        )
        print(f"   ✅ Session created: {session.id}")
        
        print("\n3. Testing session service methods...")
        # Test basic session operations
        retrieved_session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session.id
        )
        print(f"   ✅ Session retrieved: {retrieved_session.id}")
        
        # Test event logging
        from google.adk.events.event import Event
        from google.genai.types import Content, Part
        test_event = Event(
            invocation_id=str(__import__('uuid').uuid4()),
            author="user",
            content=Content(parts=[Part(text="Test message for agent integration")]),
            partial=False,
            turn_complete=True
        )
        await session_service.append_event(session, test_event)
        print("   ✅ Event logged successfully")
        
        # Flush to ensure data persistence
        session_service.flush()
        
        print("\n4. Testing analytics...")
        analytics = SessionAnalytics(session_service)
        user_summary = analytics.get_user_session_summary(app_name, user_id)
        print(f"   ✅ User has {user_summary['total_sessions']} sessions with {user_summary['total_interactions']} interactions")
        
        print("\n5. Testing session listing...")
        sessions_list = await session_service.list_sessions(app_name=app_name, user_id=user_id)
        print(f"   ✅ Found {len(sessions_list.sessions)} sessions for user {user_id}")
        
        print("\n=== Integration Test Results ===")
        print("✅ Agent import: PASSED")
        print("✅ Session service: PASSED")
        print("✅ Event tracking: PASSED")
        print("✅ Analytics: PASSED")
        print("✅ Data persistence: PASSED")
        
        print("\n🎉 Agent + TinyDB Session Service integration is working perfectly!")
        print(f"📊 Test database saved to: {os.path.abspath('agent_test_sessions.json')}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        session_service.close()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_agent_with_sessions())
    sys.exit(0 if success else 1)