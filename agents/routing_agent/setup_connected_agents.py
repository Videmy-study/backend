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

"""Setup script for connecting the Routing Agent with existing specialized agents."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
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
    """Check if the specialized agent directories exist and are properly structured."""
    print("\n🔍 Checking for specialized agents...")
    
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    academic_research_path = backend_dir / "academic-research"
    fomc_research_path = backend_dir / "fomc-research"
    
    agents_found = []
    
    # Check Academic Research Agent
    if academic_research_path.exists():
        agent_file = academic_research_path / "academic_research" / "agent.py"
        init_file = academic_research_path / "academic_research" / "__init__.py"
        if agent_file.exists() and init_file.exists():
            print(f"✅ Academic Research Agent found at: {academic_research_path}")
            agents_found.append("academic-research")
        else:
            print(f"⚠️  Academic Research Agent directory exists but files missing:")
            print(f"   agent.py: {'✅' if agent_file.exists() else '❌'} {agent_file}")
            print(f"   __init__.py: {'✅' if init_file.exists() else '❌'} {init_file}")
    else:
        print(f"⚠️  Academic Research Agent not found at: {academic_research_path}")
    
    # Check FOMC Research Agent
    if fomc_research_path.exists():
        agent_file = fomc_research_path / "fomc_research" / "agent.py"
        init_file = fomc_research_path / "fomc_research" / "__init__.py"
        if agent_file.exists() and init_file.exists():
            print(f"✅ FOMC Research Agent found at: {fomc_research_path}")
            agents_found.append("fomc-research")
        else:
            print(f"⚠️  FOMC Research Agent directory exists but files missing:")
            print(f"   agent.py: {'✅' if agent_file.exists() else '❌'} {agent_file}")
            print(f"   __init__.py: {'✅' if init_file.exists() else '❌'} {init_file}")
    else:
        print(f"⚠️  FOMC Research Agent not found at: {fomc_research_path}")
    
    return agents_found

def install_routing_agent_dependencies():
    """Install the routing agent dependencies."""
    print("\n📦 Installing routing agent dependencies...")
    
    current_dir = Path(__file__).parent
    
    try:
        subprocess.run(["poetry", "install"], cwd=current_dir, check=True)
        print("✅ Routing agent dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install routing agent dependencies: {e}")
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

def test_agent_imports():
    """Test if the routing agent can import the specialized agents."""
    print("\n🧪 Testing agent imports...")
    
    try:
        # Test if the routing agent can be imported
        from routing_agent.agent import routing_agent
        print("✅ Routing agent imported successfully")
        
        # Test if specialized agents are available
        from routing_agent.agent import AGENTS_AVAILABLE
        if AGENTS_AVAILABLE:
            print("✅ Specialized agents are available and can be imported")
            
            # Test specific imports
            try:
                from academic_research import academic_coordinator
                print("✅ Academic Research Agent imported successfully")
            except ImportError as e:
                print(f"⚠️  Academic Research Agent import failed: {e}")
            
            try:
                from fomc_research import root_agent as fomc_agent
                print("✅ FOMC Research Agent imported successfully")
            except ImportError as e:
                print(f"⚠️  FOMC Research Agent import failed: {e}")
        else:
            print("⚠️  Specialized agents are not available")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import routing agent: {e}")
        return False

def create_workspace_setup():
    """Create a workspace setup that includes all agents."""
    print("\n🏗️  Creating workspace setup...")
    
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    
    # Create a workspace pyproject.toml that includes all agents
    workspace_pyproject = backend_dir / "pyproject.toml"
    
    workspace_config = f"""[tool.poetry]
name = "videmy-study-agents"
version = "0.1.0"
description = "Connected agents for academic and financial research"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
google-adk = "^1.0.0"
google-genai = "^1.9.0"
google-cloud-aiplatform = {{ version = "^1.93", extras = ["adk", "agent-engines"] }}

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
pytest-asyncio = "^0.26.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    
    with open(workspace_pyproject, "w") as f:
        f.write(workspace_config)
    
    print(f"✅ Created workspace configuration at {workspace_pyproject}")
    return True

def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Setup Connected Agents")
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
        help="Skip testing the agent imports"
    )
    parser.add_argument(
        "--create-workspace",
        action="store_true",
        help="Create a workspace setup for all agents"
    )
    
    args = parser.parse_args()
    
    print("🚀 Setting up Connected Agents...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Check for specialized agents
    agents_found = check_agent_directories()
    if not agents_found:
        print("\n⚠️  No specialized agents found. The routing agent will work but won't be able to route to specialized agents.")
        print("   Please ensure academic-research and fomc-research agents are in the backend directory.")
    
    # Install routing agent dependencies
    if not install_routing_agent_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment(args.project_id, args.location):
        sys.exit(1)
    
    # Create workspace setup if requested
    if args.create_workspace:
        create_workspace_setup()
    
    # Test the agent imports
    if not args.skip_tests:
        if not test_agent_imports():
            print("\n⚠️  Agent import test failed, but setup completed. You may need to check the configuration.")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Run the routing agent locally:")
    print("   cd backend/routing_agent")
    print("   poetry shell")
    print("   adk run routing_agent")
    print("\n2. Or use the web interface:")
    print("   adk web")
    print("\n3. Test with different types of queries:")
    print("   - Academic: 'I need help analyzing this research paper'")
    print("   - FOMC: 'What was the impact of the latest Fed meeting?'")
    print("\n📚 For more information, see the README.md file")

if __name__ == "__main__":
    main() 