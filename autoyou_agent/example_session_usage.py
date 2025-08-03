#!/usr/bin/env python3
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

"""Example usage of TinyDB session service and analytics.

This script demonstrates how to:
1. Access session data stored by the autoyou_agent
2. Analyze user interactions and agent responses
3. Generate reports on agent usage patterns
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from tinydb_session_service import TinyDBSessionService
from session_analytics import SessionAnalytics, create_analytics_instance


async def demonstrate_session_analytics():
    """Demonstrate session analytics capabilities."""
    print("=== AutoYou Agent Session Analytics Demo ===")
    print()
    
    # Create analytics instance
    analytics = create_analytics_instance("autoyou_sessions.json")
    
    # Check if we have any data
    session_service = analytics.session_service
    all_sessions = session_service.sessions_table.all()
    
    if not all_sessions:
        print("No session data found. Start using the autoyou_agent to generate data.")
        return
    
    print(f"Found {len(all_sessions)} sessions in the database.")
    print()
    
    # Get unique app names and user IDs
    app_names = set([s['app_name'] for s in all_sessions])
    user_ids = set([s['user_id'] for s in all_sessions])
    
    print(f"Apps: {', '.join(app_names)}")
    print(f"Users: {', '.join(user_ids)}")
    print()
    
    # Analyze each user
    for app_name in app_names:
        for user_id in user_ids:
            user_sessions = [s for s in all_sessions 
                           if s['app_name'] == app_name and s['user_id'] == user_id]
            
            if not user_sessions:
                continue
                
            print(f"=== Analysis for User: {user_id} in App: {app_name} ===")
            
            # Get user session summary
            summary = analytics.get_user_session_summary(app_name, user_id)
            print_user_summary(summary)
            
            # Analyze individual sessions
            for session in user_sessions[:3]:  # Limit to first 3 sessions
                session_id = session['id']
                print(f"\n--- Session Analysis: {session_id} ---")
                
                patterns = analytics.detect_conversation_patterns(app_name, user_id, session_id)
                print_conversation_patterns(patterns)
                
                # Get interaction summary
                interaction_summary = session_service.get_agent_interaction_summary(
                    app_name, user_id, session_id
                )
                print_interaction_summary(interaction_summary)
            
            print("\n" + "="*60 + "\n")
    
    # Get app-wide statistics
    for app_name in app_names:
        print(f"=== Agent Usage Statistics for {app_name} ===")
        usage_stats = analytics.get_agent_usage_statistics(app_name, days=30)
        print_usage_statistics(usage_stats)
        print()
        
        # Get frequent questions
        print(f"=== Frequent User Questions in {app_name} ===")
        frequent_questions = analytics.get_frequent_user_questions(app_name, limit=10)
        print_frequent_questions(frequent_questions)
        print()


def print_user_summary(summary: Dict[str, Any]):
    """Print user session summary."""
    print(f"Total Sessions: {summary['total_sessions']}")
    print(f"Total Interactions: {summary['total_interactions']}")
    print(f"User Questions: {summary['user_questions']}")
    print(f"Agent Responses: {summary['agent_responses']}")
    print(f"Agent Transfers: {summary['agent_transfers']}")
    
    if summary['most_used_agents']:
        print("\nMost Used Agents:")
        for agent, count in list(summary['most_used_agents'].items())[:5]:
            print(f"  - {agent}: {count} times")
    
    if summary['daily_activity']:
        print("\nDaily Activity (last 10 days):")
        sorted_days = sorted(summary['daily_activity'].items(), reverse=True)[:10]
        for date, count in sorted_days:
            print(f"  - {date}: {count} sessions")


def print_conversation_patterns(patterns: Dict[str, Any]):
    """Print conversation pattern analysis."""
    print(f"Total Interactions: {patterns['total_interactions']}")
    print(f"Conversation Duration: {patterns['conversation_duration']:.2f} seconds")
    
    if patterns['agents_involved']:
        print(f"Agents Involved: {', '.join(patterns['agents_involved'])}")
    
    if patterns['transfer_sequence']:
        print(f"Transfer Sequence: {' -> '.join(patterns['transfer_sequence'])}")
    
    if patterns['detected_loops']:
        print("\nDetected Transfer Loops:")
        for loop in patterns['detected_loops']:
            print(f"  - Pattern: {' -> '.join(loop['pattern'])} (repeated {loop['repetitions']} times)")
    
    if patterns['question_response_pairs']:
        print(f"\nQuestion-Response Pairs: {len(patterns['question_response_pairs'])}")
        avg_response_time = sum([p['duration_seconds'] for p in patterns['question_response_pairs']]) / len(patterns['question_response_pairs'])
        print(f"Average Response Time: {avg_response_time:.2f} seconds")


def print_interaction_summary(summary: Dict[str, Any]):
    """Print interaction summary."""
    print(f"Interaction Summary:")
    print(f"  - Total: {summary['total_interactions']}")
    print(f"  - Questions: {summary['user_questions']}")
    print(f"  - Responses: {summary['agent_responses']}")
    print(f"  - Transfers: {summary['agent_transfers']}")
    
    if summary['agents_used']:
        print(f"  - Agents Used: {', '.join(summary['agents_used'])}")


def print_usage_statistics(stats: Dict[str, Any]):
    """Print agent usage statistics."""
    print(f"Analysis Period: {stats['analysis_period_days']} days")
    print(f"Total Interactions: {stats['total_interactions']}")
    print(f"Total Transfers: {stats['total_transfers']}")
    
    if stats['most_popular_agents']:
        print("\nMost Popular Agents:")
        for agent, count in list(stats['most_popular_agents'].items())[:5]:
            print(f"  - {agent}: {count} transfers")
    
    if stats['agent_user_counts']:
        print("\nAgent User Engagement:")
        sorted_agents = sorted(stats['agent_user_counts'].items(), key=lambda x: x[1], reverse=True)[:5]
        for agent, user_count in sorted_agents:
            print(f"  - {agent}: {user_count} unique users")


def print_frequent_questions(questions: list):
    """Print frequent user questions."""
    if not questions:
        print("No frequent questions found.")
        return
    
    for i, q in enumerate(questions[:5], 1):
        print(f"{i}. \"{q['example_full_question']}\" (asked {q['frequency']} times by {q['users_asked']} users)")


async def export_session_example():
    """Example of exporting session data."""
    print("\n=== Session Data Export Example ===")
    
    analytics = create_analytics_instance("autoyou_sessions.json")
    session_service = analytics.session_service
    
    # Get the most recent session
    all_sessions = session_service.sessions_table.all()
    if not all_sessions:
        print("No sessions to export.")
        return
    
    # Sort by creation time and get the most recent
    recent_session = max(all_sessions, key=lambda x: x['created_at'])
    
    app_name = recent_session['app_name']
    user_id = recent_session['user_id']
    session_id = recent_session['id']
    
    print(f"Exporting session: {session_id}")
    
    # Export session data
    export_data = analytics.export_session_data(app_name, user_id, session_id)
    
    # Save to file
    export_filename = f"session_export_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(export_filename, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"Session data exported to: {export_filename}")
    print(f"Export contains:")
    print(f"  - Session info: {1 if export_data['session'] else 0} record")
    print(f"  - Events: {len(export_data['events'])} records")
    print(f"  - Interactions: {len(export_data['interactions'])} records")


if __name__ == "__main__":
    print("AutoYou Agent Session Analytics")
    print("==============================")
    print()
    
    # Run the demonstration
    asyncio.run(demonstrate_session_analytics())
    
    # Run export example
    asyncio.run(export_session_example())
    
    print("\nDemo completed. Check the generated files for exported data.")