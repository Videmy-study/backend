#!/usr/bin/env python3
"""
Setup script for the routing agent and its dependencies.
This script installs the routing agent and its dependencies properly.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_routing_agent():
    """Setup the routing agent and its dependencies."""
    print("🔧 Setting up routing agent...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    routing_agent_dir = current_dir / "agents" / "routing-agent"
    
    if not routing_agent_dir.exists():
        print("❌ Routing agent directory not found!")
        return False
    
    print(f"📍 Routing agent directory: {routing_agent_dir}")
    
    # Check if pyproject.toml exists
    pyproject_file = routing_agent_dir / "pyproject.toml"
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found in routing agent directory!")
        return False
    
    # Install the routing agent in development mode
    print("📦 Installing routing agent...")
    result = run_command("pip install -e .", cwd=routing_agent_dir)
    
    if result is None:
        print("❌ Failed to install routing agent!")
        return False
    
    print("✅ Routing agent installed successfully!")
    
    # Test the import
    print("🧪 Testing routing agent import...")
    try:
        sys.path.insert(0, str(routing_agent_dir))
        from routing_agent.routing_agent.agent import routing_agent
        print("✅ Routing agent import successful!")
        return True
    except ImportError as e:
        print(f"❌ Routing agent import failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Videmy Study Routing Agent Setup")
    print("=" * 50)
    
    success = setup_routing_agent()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("The routing agent is now ready to use.")
    else:
        print("\n⚠️ Setup completed with warnings.")
        print("The app will run in simulation mode.")
    
    print("\n📝 Next steps:")
    print("1. Restart your application")
    print("2. Test the /chat endpoint")
    print("3. Check the logs for any remaining issues")

if __name__ == "__main__":
    main() 