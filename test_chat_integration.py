#!/usr/bin/env python3
"""
Test script for the chat integration with ADK routing agent.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from managers.chat_manager_clean import chat_manager

async def test_chat_integration():
    """Test the chat integration with various message types."""
    
    print("🧪 Testing Chat Integration with ADK Routing Agent")
    print("=" * 60)
    
    # Test messages for different routing scenarios
    test_messages = [
        {
            "message": "I need help with academic research on machine learning",
            "expected_agent": "academic_coordinator",
            "description": "Academic research query"
        },
        {
            "message": "What's the latest FOMC decision on interest rates?",
            "expected_agent": "fomc_research_agent", 
            "description": "FOMC/economic policy query"
        },
        {
            "message": "Tell me about the latest political news",
            "expected_agent": "political_news_coordinator",
            "description": "Political news query"
        },
        {
            "message": "Hello, how are you?",
            "expected_agent": "general_assistant",
            "description": "General greeting"
        }
    ]
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"Message: {test_case['message']}")
        print(f"Expected agent: {test_case['expected_agent']}")
        
        try:
            # Process the message
            result = await chat_manager.process_chat_message(
                message=test_case['message'],
                user_id="test_user_123"
            )
            
            # Display results
            print(f"✅ Success: {result['success']}")
            print(f"🤖 Agent used: {result['agent_used']}")
            print(f"🎯 Routing reason: {result['routing_reason']}")
            print(f"💬 Response: {result['response'][:100]}...")
            
            if 'tool_calls' in result and result['tool_calls']:
                print(f"🔧 Tool calls: {result['tool_calls']}")
            
            if 'session_id' in result and result['session_id']:
                print(f"🆔 Session ID: {result['session_id']}")
            
            # Check if routing worked as expected (for simulation mode)
            if result['agent_used'] == test_case['expected_agent']:
                print("✅ Routing worked as expected!")
            else:
                print(f"⚠️ Routing different than expected (got {result['agent_used']})")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n🎉 Chat integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_chat_integration()) 