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

"""Setup script for the Routing Agent."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        return False
    
    # Check if poetry is installed
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        print("✅ Poetry is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Poetry is not installed. Please install it first:")
        print("   pip install poetry")
        return False
    
    # Check if gcloud is installed
    try:
        subprocess.run(["gcloud", "--version"], check=True, capture_output=True)
        print("✅ Google Cloud CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Google Cloud CLI is not installed. Please install it first:")
        print("   https://cloud.google.com/sdk/docs/install")
        return False
    
    return True

def check_agent_directories():
    """Check if the specialized agent directories exist."""
    print("\n🔍 Checking for specialized agents...")
    
    current_dir = Path(__file__).parent
    academic_research_path = current_dir.parent / "academic-research"
    fomc_research_path = current_dir.parent / "fomc-research"
    
    agents_found = []
    
    if academic_research_path.exists():
        print(f"✅ Academic Research Agent found at: {academic_research_path}")
        agents_found.append("academic-research")
    else:
        print(f"⚠️  Academic Research Agent not found at: {academic_research_path}")
    
    if fomc_research_path.exists():
        print(f"✅ FOMC Research Agent found at: {fomc_research_path}")
        agents_found.append("fomc-research")
    else:
        print(f"⚠️  FOMC Research Agent not found at: {fomc_research_path}")
    
    return agents_found

def install_dependencies():
    """Install the routing agent dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run(["poetry", "add", "../academic_research", "../fomc_research", "../political_news"], check=True)
        subprocess.run(["poetry", "install"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment(project_id: str, location: str):
    """Set up environment variables."""
    print(f"\n🔧 Setting up environment...")
    
    env_vars = {
        "GOOGLE_GENAI_USE_VERTEXAI": "true",
        "GOOGLE_CLOUD_PROJECT": project_id,
        "GOOGLE_CLOUD_LOCATION": location,
    }
    
    # Create .env file
    env_file = Path(__file__).parent / ".env"
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ Environment variables saved to {env_file}")
    
    # Print instructions for manual setup
    print("\n📋 Manual setup instructions:")
    print("1. Authenticate with Google Cloud:")
    print(f"   gcloud auth application-default login")
    print(f"   gcloud auth application-default set-quota-project {project_id}")
    print("\n2. Enable required APIs:")
    print("   gcloud services enable aiplatform.googleapis.com")
    print("   gcloud services enable agentengine.googleapis.com")
    
    return True

def test_agent():
    """Test the routing agent."""
    print("\n🧪 Testing the routing agent...")
    
    try:
        # Test if the agent can be imported
        from routing_agent.agent import routing_agent
        print("✅ Routing agent imported successfully")
        
        # Test if specialized agents are available
        from routing_agent.agent import AGENTS_AVAILABLE
        if AGENTS_AVAILABLE:
            print("✅ Specialized agents are available")
        else:
            print("⚠️  Specialized agents are not available")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import routing agent: {e}")
        return False

def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Setup Routing Agent")
    parser.add_argument(
        "--project-id",
        required=True,
        help="Google Cloud project ID"
    )
    parser.add_argument(
        "--location",
        default="us-central1",
        help="Google Cloud location (default: us-central1)"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip testing the agent"
    )
    
    args = parser.parse_args()
    
    print("🚀 Setting up Routing Agent...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Check for specialized agents
    agents_found = check_agent_directories()
    if not agents_found:
        print("\n⚠️  No specialized agents found. The routing agent will work but won't be able to route to specialized agents.")
        print("   Please ensure academic-research and fomc-research agents are in the parent directory.")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment(args.project_id, args.location):
        sys.exit(1)
    
    # Test the agent
    if not args.skip_tests:
        if not test_agent():
            print("\n⚠️  Agent test failed, but setup completed. You may need to check the configuration.")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Run the agent locally:")
    print("   adk run routing_agent")
    print("\n2. Or use the web interface:")
    print("   adk web")
    print("\n3. Deploy to production:")
    print(f"   python deployment/deploy.py --project-id {args.project_id} --location {args.location}")
    print("\n📚 For more information, see the README.md file")

if __name__ == "__main__":
    main() 