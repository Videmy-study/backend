#!/usr/bin/env python3
"""Simple test script to verify routing agent imports work correctly."""

import sys
import os
from pathlib import Path

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not available, .env file not loaded")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

# Add parent directories to path
current_dir = Path(__file__).parent
backend_dir = current_dir.parent
academic_research_path = backend_dir / "academic-research"
fomc_research_path = backend_dir / "fomc-research"

print("🔍 Testing routing agent imports...")
print(f"Current directory: {current_dir}")
print(f"Backend directory: {backend_dir}")

# Check environment variables
print("\n🔧 Environment check:")
print(f"   GOOGLE_GENAI_USE_VERTEXAI: {os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'Not set')}")
print(f"   GOOGLE_API_KEY: {'Set' if os.getenv('GOOGLE_API_KEY') else 'Not set'}")
print(f"   GOOGLE_PLACES_API_KEY: {'Set' if os.getenv('GOOGLE_PLACES_API_KEY') else 'Not set'}")

# Add paths to sys.path
if academic_research_path.exists():
    sys.path.insert(0, str(academic_research_path))
    print("✅ Added academic-research to sys.path")
else:
    print("❌ academic-research path not found")

if fomc_research_path.exists():
    sys.path.insert(0, str(fomc_research_path))
    print("✅ Added fomc-research to sys.path")
else:
    print("❌ fomc-research path not found")

print("\n🧪 Testing routing agent import...")

# Test routing agent import (this should work even if specialized agents fail)
try:
    from routing_agent.agent import routing_agent, AGENTS_AVAILABLE
    print("✅ Successfully imported routing_agent")
    print(f"   Name: {routing_agent.name}")
    print(f"   Description: {routing_agent.description}")
    print(f"   Specialized agents available: {AGENTS_AVAILABLE}")
    
    if AGENTS_AVAILABLE:
        print("   ✅ Specialized agents are available")
        print(f"   📋 Number of tools: {len(routing_agent.tools)}")
        for i, tool in enumerate(routing_agent.tools):
            if hasattr(tool, 'agent') and tool.agent:
                print(f"   📋 Tool {i+1}: {tool.agent.name}")
    else:
        print("   ⚠️  Specialized agents are not available")
        print("   💡 This may be due to missing API keys or authentication issues")
        
except ImportError as e:
    print(f"❌ Failed to import routing_agent: {e}")
    print("\n💡 Troubleshooting:")
    print("1. Make sure you have a .env file with your API keys")
    print("2. Run: python create_env.py to create a .env file template")
    print("3. Install python-dotenv: pip install python-dotenv")

print("\n✅ Routing agent import test completed!") 