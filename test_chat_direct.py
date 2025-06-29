#!/usr/bin/env python3
"""
Direct test of the chat manager to verify it's working properly.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from managers.chat_manager import chat_manager

async def test_chat_manager():
    """Test the chat manager directly."""
    print("🧪 Testing Chat Manager Directly")
    print("=" * 50)
    
    # Test messages
    test_messages = [
        "I need help with academic research on machine learning",
        "What's the latest FOMC news and its impact on markets?",
        "Tell me about the latest political news",
        "Hello, how can you help me?",
        "I want to understand economic policy research"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}: '{message}'")
        print("-" * 40)
        
        try:
            response = await chat_manager.process_chat_message(
                message=message,
                user_id=f"test_user_{i}",
                session_id=f"test_session_{i}"
            )
            
            print(f"✅ Success: {response['success']}")
            print(f"📝 Message: {response['message']}")
            print(f"🤖 Response: {response['response'][:200]}...")
            print(f"🔧 Agent Used: {response['agent_used']}")
            print(f"🎯 Routing Reason: {response['routing_reason']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Chat manager test completed!")

async def main():
    """Main test function."""
    print("🚀 Videmy Study Chat Manager Test")
    print("=" * 50)
    
    await test_chat_manager()
    
    print("\n📝 Summary:")
    print("✅ Chat manager test completed!")
    print("✅ Check if responses are dynamic or still hardcoded")

if __name__ == "__main__":
    asyncio.run(main()) 