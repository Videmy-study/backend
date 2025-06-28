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

"""Test script to verify the routing agent can connect to specialized agents."""

import sys
from pathlib import Path

def test_agent_connection():
    """Test if the routing agent can connect to the specialized agents."""
    print("🧪 Testing Agent Connection...")
    print("=" * 50)
    
    try:
        # Test routing agent import
        print("1. Testing routing agent import...")
        from routing_agent.agent import routing_agent, AGENTS_AVAILABLE
        print("   ✅ Routing agent imported successfully")
        
        # Test specialized agents availability
        print("\n2. Testing specialized agents availability...")
        if AGENTS_AVAILABLE:
            print("   ✅ Specialized agents are available")
            
            # Test academic research agent
            print("\n3. Testing Academic Research Agent...")
            try:
                from academic_research import academic_coordinator
                print("   ✅ Academic Research Agent imported successfully")
                print(f"   📋 Agent name: {academic_coordinator.name}")
                print(f"   📋 Agent description: {academic_coordinator.description}")
            except ImportError as e:
                print(f"   ❌ Academic Research Agent import failed: {e}")
            
            # Test FOMC research agent
            print("\n4. Testing FOMC Research Agent...")
            try:
                from fomc_research import root_agent as fomc_agent
                print("   ✅ FOMC Research Agent imported successfully")
                print(f"   📋 Agent name: {fomc_agent.name}")
                print(f"   📋 Agent description: {fomc_agent.description}")
            except ImportError as e:
                print(f"   ❌ FOMC Research Agent import failed: {e}")
            
            # Test routing agent tools
            print("\n5. Testing routing agent tools...")
            tools = routing_agent.tools
            print(f"   📋 Number of tools available: {len(tools)}")
            for i, tool in enumerate(tools):
                print(f"   📋 Tool {i+1}: {tool.agent.name if hasattr(tool, 'agent') else 'Unknown'}")
            
        else:
            print("   ❌ Specialized agents are not available")
            print("   💡 Make sure academic-research and fomc-research directories exist")
        
        print("\n" + "=" * 50)
        print("✅ Connection test completed!")
        
        if AGENTS_AVAILABLE:
            print("\n🎯 Ready to use! You can now:")
            print("1. Run: adk run routing_agent")
            print("2. Ask academic questions: 'I need help analyzing this research paper'")
            print("3. Ask FOMC questions: 'What was the impact of the latest Fed meeting?'")
        else:
            print("\n⚠️  Setup incomplete. Please run the setup script:")
            print("   python setup_connected_agents.py --project-id YOUR_PROJECT_ID")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure you're running this from the routing-agent directory")
        print("   cd backend/routing-agent")
        print("   poetry shell")
        print("   python test_connection.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_directory_structure():
    """Show the current directory structure."""
    print("\n📁 Current Directory Structure:")
    print("=" * 30)
    
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    
    print(f"Current directory: {current_dir}")
    print(f"Backend directory: {backend_dir}")
    
    # Check for specialized agents
    academic_path = backend_dir / "academic-research"
    fomc_path = backend_dir / "fomc-research"
    
    print(f"\nAcademic Research: {'✅' if academic_path.exists() else '❌'} {academic_path}")
    print(f"FOMC Research: {'✅' if fomc_path.exists() else '❌'} {fomc_path}")
    
    if academic_path.exists():
        agent_file = academic_path / "academic_research" / "academic_research" / "agent.py"
        init_file = academic_path / "academic_research" / "__init__.py"
        print(f"  Academic agent.py: {'✅' if agent_file.exists() else '❌'} {agent_file}")
        print(f"  Academic __init__.py: {'✅' if init_file.exists() else '❌'} {init_file}")
    
    if fomc_path.exists():
        agent_file = fomc_path / "fomc_research" / "fomc_research" / "agent.py"
        init_file = fomc_path / "fomc_research" / "__init__.py"
        print(f"  FOMC agent.py: {'✅' if agent_file.exists() else '❌'} {agent_file}")
        print(f"  FOMC __init__.py: {'✅' if init_file.exists() else '❌'} {init_file}")

if __name__ == "__main__":
    print("🚀 Testing Routing Agent Connection")
    print("=" * 50)
    
    # Show directory structure
    show_directory_structure()
    
    # Test connection
    success = test_agent_connection()
    
    if not success:
        sys.exit(1) 