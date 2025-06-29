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

"""Deployment script for the Routing Agent."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def deploy_agent(project_id: str, location: str, agent_id: str = "routing-agent"):
    """Deploy the routing agent to Google Agent Engine.
    
    Args:
        project_id: Google Cloud project ID
        location: Google Cloud location (e.g., us-central1)
        agent_id: Agent ID for deployment
    """
    
    # Get the current directory
    current_dir = Path(__file__).parent.parent
    
    # Set environment variables
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = location
    
    print(f"Deploying routing agent to project: {project_id}")
    print(f"Location: {location}")
    print(f"Agent ID: {agent_id}")
    
    try:
        # Build the agent package
        print("Building agent package...")
        subprocess.run([
            "poetry", "build"
        ], cwd=current_dir, check=True)
        
        # Deploy using ADK
        print("Deploying to Agent Engine...")
        subprocess.run([
            "adk", "deploy", 
            "--project-id", project_id,
            "--location", location,
            "--agent-id", agent_id
        ], cwd=current_dir, check=True)
        
        print(f"✅ Successfully deployed routing agent with ID: {agent_id}")
        print(f"Agent is now available at: https://console.cloud.google.com/vertex-ai/agents/{agent_id}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during deployment: {e}")
        sys.exit(1)

def main():
    """Main function for deployment script."""
    parser = argparse.ArgumentParser(description="Deploy Routing Agent to Google Agent Engine")
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
        "--agent-id",
        default="routing-agent",
        help="Agent ID for deployment (default: routing-agent)"
    )
    
    args = parser.parse_args()
    
    deploy_agent(args.project_id, args.location, args.agent_id)

if __name__ == "__main__":
    main() 