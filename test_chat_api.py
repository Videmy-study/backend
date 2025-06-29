#!/usr/bin/env python3
"""
Test script for the Videmy Study Chat API endpoints.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

# API base URL (adjust as needed)
BASE_URL = "http://localhost:8000"

async def test_chat_endpoint(session: aiohttp.ClientSession, message: str, user_id: str = None) -> Dict[str, Any]:
    """Test the /chat endpoint."""
    url = f"{BASE_URL}/chat"
    
    payload = {
        "message": message,
        "user_id": user_id,
        "session_id": "test_session"
    }
    
    try:
        async with session.post(url, json=payload) as response:
            result = await response.json()
            print(f"\n📝 Test Message: {message}")
            print(f"✅ Status: {response.status}")
            print(f"🤖 Response: {result.get('response', 'No response')}")
            print(f"🔧 Agent Used: {result.get('agent_used', 'None')}")
            print(f"🎯 Routing Reason: {result.get('routing_reason', 'None')}")
            return result
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
        return {"error": str(e)}

async def test_agents_endpoint(session: aiohttp.ClientSession) -> Dict[str, Any]:
    """Test the /chat/agents endpoint."""
    url = f"{BASE_URL}/chat/agents"
    
    try:
        async with session.get(url) as response:
            result = await response.json()
            print(f"\n🔍 Available Agents:")
            print(f"✅ Status: {response.status}")
            print(f"📋 Agents: {result.get('available_agents', [])}")
            print(f"📊 Total: {result.get('total_agents', 0)}")
            print(f"🟢 Service Status: {result.get('service_status', 'unknown')}")
            return result
    except Exception as e:
        print(f"❌ Error testing agents endpoint: {e}")
        return {"error": str(e)}

async def test_health_endpoint(session: aiohttp.ClientSession) -> Dict[str, Any]:
    """Test the /chat/health endpoint."""
    url = f"{BASE_URL}/chat/health"
    
    try:
        async with session.get(url) as response:
            result = await response.json()
            print(f"\n🏥 Chat Health Check:")
            print(f"✅ Status: {response.status}")
            print(f"🟢 Chat Service: {result.get('chat_service', 'unknown')}")
            print(f"📊 Available Agents: {result.get('available_agents', 0)}")
            print(f"🟢 Overall Status: {result.get('status', 'unknown')}")
            return result
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return {"error": str(e)}

async def main():
    """Run all tests."""
    print("🧪 Testing Videmy Study Chat API")
    print("=" * 50)
    
    # Test messages for different agent types
    test_messages = [
        "I need help analyzing a research paper on machine learning",
        "What was the impact of the latest Fed meeting on markets?",
        "What's the latest news on the Israel-Palestine conflict?",
        "Hello, how can you help me?",
        "I want to understand economic policy research"
    ]
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint first
        print("\n1️⃣ Testing Health Endpoint...")
        await test_health_endpoint(session)
        
        # Test agents endpoint
        print("\n2️⃣ Testing Agents Endpoint...")
        await test_agents_endpoint(session)
        
        # Test chat endpoint with different messages
        print("\n3️⃣ Testing Chat Endpoint...")
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Test {i} ---")
            await test_chat_endpoint(session, message, f"test_user_{i}")
            await asyncio.sleep(1)  # Small delay between requests
    
    print("\n🎉 Chat API testing completed!")

if __name__ == "__main__":
    asyncio.run(main()) 