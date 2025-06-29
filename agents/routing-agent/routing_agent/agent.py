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

"""Routing Agent: Routes user requests to appropriate specialized agents."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

MODEL = "gemini-2.5-pro"

# Load environment variables from multiple locations
def load_environment_variables():
    """Load environment variables from routing agent and political news directories."""
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent.parent
    agents_dir = backend_dir / "agents"
    
    # Load from routing agent directory
    routing_env_file = backend_dir / "routing-agent" / ".env"
    if routing_env_file.exists():
        load_dotenv(routing_env_file)
        print(f"✅ Loaded environment variables from {routing_env_file}")
    
    # Load from political news directory
    political_env_file = agents_dir / "political-news" / ".env"
    if political_env_file.exists():
        load_dotenv(political_env_file)
        print(f"✅ Loaded environment variables from {political_env_file}")
    
    # Check for required political news API keys
    political_keys = ["NEWSAPI_KEY", "GNEWS_API_KEY", "MEDIASTACK_API_KEY", "NEWSDATA_API_KEY"]
    available_keys = [key for key in political_keys if os.getenv(key)]
    
    if available_keys:
        print(f"✅ Found {len(available_keys)} political news API keys: {', '.join(available_keys)}")
    else:
        print("⚠️  No political news API keys found. Political news agent may not work properly.")
        print("   Please set at least one of: NEWSAPI_KEY, GNEWS_API_KEY, MEDIASTACK_API_KEY, NEWSDATA_API_KEY")

# Load environment variables
load_environment_variables()

# Add parent directories to path to import the specialized agents
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent.parent  # Go up 3 levels: routing_agent -> routing-agent -> agents -> backend
agents_dir = backend_dir / "agents"
academic_research_path = agents_dir / "academic-research"
fomc_research_path = agents_dir / "fomc-research"
political_news_path = agents_dir / "political-news"

# Add paths to sys.path for imports
if academic_research_path.exists():
    sys.path.insert(0, str(academic_research_path))
if fomc_research_path.exists():
    sys.path.insert(0, str(fomc_research_path))
if political_news_path.exists():
    sys.path.insert(0, str(political_news_path))

# Import the specialized agents with error handling
AGENTS_AVAILABLE = False
academic_coordinator = None
fomc_research_agent = None
political_news_coordinator = None

try:
    from academic_research import academic_coordinator
    print("✅ Successfully imported Academic Research Agent")
except ImportError as e:
    print(f"⚠️  Warning: Could not import Academic Research Agent: {e}")
    print("   This may be due to missing dependencies or authentication issues")

try:
    from fomc_research import fomc_research_agent
    print("✅ Successfully imported FOMC Research Agent")
    print("   Note: BigQuery functionality may not be available without proper credentials")
except ImportError as e:
    print(f"⚠️  Warning: Could not import FOMC Research Agent: {e}")
    print("   This may be due to missing dependencies or authentication issues")
    print("   The FOMC agent requires Google Cloud authentication to be set up")

try:
    from political_news import political_news_coordinator
    print("✅ Successfully imported Political News Agent")
except ImportError as e:
    print(f"⚠️  Warning: Could not import Political News Agent: {e}")
    print("   This may be due to missing dependencies or API key issues")

# Check if agents are available
available_agents = []
if academic_coordinator is not None:
    available_agents.append("Academic Research")
if fomc_research_agent is not None:
    available_agents.append("FOMC Research")
if political_news_coordinator is not None:
    available_agents.append("Political News")

if len(available_agents) >= 2:
    AGENTS_AVAILABLE = True
    print(f"✅ Multiple specialized agents are available for routing: {', '.join(available_agents)}")
elif len(available_agents) == 1:
    print(f"✅ {available_agents[0]} Agent is available for routing")
    print("⚠️  Other agents are not available")
else:
    print("⚠️  No specialized agents are available")
    print("   The routing agent will still work but with limited functionality")

# Create tools list with available agents
tools = []
if academic_coordinator is not None:
    tools.append(AgentTool(agent=academic_coordinator))
if fomc_research_agent is not None:
    tools.append(AgentTool(agent=fomc_research_agent))
if political_news_coordinator is not None:
    tools.append(AgentTool(agent=political_news_coordinator))

routing_agent = LlmAgent(
    name="routing_agent",
    model=MODEL,
    description=(
        "A routing agent that analyzes user requests and directs them to the appropriate "
        "specialized agent - academic research, FOMC financial analysis, or political news."
    ),
    instruction=prompt.ROUTING_AGENT_PROMPT,
    output_key="routed_response",
    tools=tools,
)

root_agent = routing_agent 