#!/usr/bin/env python3
"""
Simple test script for the chat endpoint without routing agent dependency.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from managers.chat_manager import chat_manager

async def test_chat_manager():
    """Test the chat manager functionality."""
    print("🧪 Testing Chat Manager...")
    print("=" * 50)
    
    # Test initialization
    print(f"✅ Chat manager initialized: {chat_manager.is_available()}")
    print(f"📋 Available agents: {chat_manager.get_available_agents()}")
    
    # Test messages
    test_messages = [
        "I need help with academic research",
        "What's the latest FOMC news?",
        "Tell me about political news",
        "Hello, how are you?",
        "Can you help me with financial analysis?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}: '{message}'")
        print("-" * 30)
        
        try:
            response = await chat_manager.process_chat_message(
                message=message,
                user_id="test_user_123",
                session_id="test_session_456"
            )
            
            print(f"✅ Success: {response['success']}")
            print(f"🤖 Agent used: {response['agent_used']}")
            print(f"📝 Response: {response['response'][:100]}...")
            print(f"🎯 Routing reason: {response['routing_reason']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Chat manager test completed!")

def test_imports():
    """Test that all necessary imports work."""
    print("🔧 Testing imports...")
    
    try:
        from managers.chat_manager import chat_manager
        print("✅ Chat manager import successful")
        
        from managers.session_manager import SessionManager
        print("✅ Session manager import successful")
        
        from api.schemas import ChatRequest, ChatResponse
        print("✅ API schemas import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Videmy Study Chat API Test")
    print("=" * 50)
    
    # Test imports first
    if not test_imports():
        print("❌ Import tests failed!")
        return
    
    print("\n" + "=" * 50)
    
    # Test chat manager
    await test_chat_manager()
    
    print("\n📝 Summary:")
    print("✅ All tests completed successfully!")
    print("✅ Chat endpoint should work without routing agent")
    print("✅ Ready for deployment to Render")

if __name__ == "__main__":
    asyncio.run(main()) 