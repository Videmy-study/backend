#!/usr/bin/env python3
"""
Test script to verify Videmy Study API deployment on Render.
"""

import requests
import json
import sys
from typing import Dict, Any

def test_endpoint(base_url: str, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a specific endpoint."""
    url = f"{base_url}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "success": False,
            "url": url
        }

def main():
    """Run deployment tests."""
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:8000"
    
    print(f"🧪 Testing Videmy Study API Deployment")
    print(f"📍 Base URL: {base_url}")
    print("=" * 60)
    
    # Test endpoints
    tests = [
        ("Health Check", "/chat/health", "GET"),
        ("Available Agents", "/chat/agents", "GET"),
        ("Root Endpoint", "/", "GET"),
        ("Chat API - Academic", "/chat", "POST", {
            "message": "I need help analyzing a research paper on machine learning",
            "user_id": "test_user_1"
        }),
        ("Chat API - Financial", "/chat", "POST", {
            "message": "What was the impact of the latest Fed meeting on markets?",
            "user_id": "test_user_2"
        }),
        ("Chat API - Political", "/chat", "POST", {
            "message": "What's the latest news on the Israel-Palestine conflict?",
            "user_id": "test_user_3"
        }),
    ]
    
    results = []
    
    for test_name, endpoint, method, *args in tests:
        print(f"\n🔍 Testing: {test_name}")
        print(f"   Endpoint: {method} {endpoint}")
        
        data = args[0] if args else None
        result = test_endpoint(base_url, endpoint, method, data)
        
        if result.get("success"):
            print(f"   ✅ Status: {result['status_code']}")
            if "data" in result and isinstance(result["data"], dict):
                if "response" in result["data"]:
                    print(f"   🤖 Response: {result['data']['response'][:100]}...")
                if "agent_used" in result["data"]:
                    print(f"   🔧 Agent: {result['data']['agent_used']}")
        else:
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
        
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    
    passed = sum(1 for _, result in results if result.get("success"))
    total = len(results)
    
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 