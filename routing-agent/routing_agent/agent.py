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

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

MODEL = "gemini-2.5-pro"

# Add parent directories to path to import the specialized agents
current_dir = Path(__file__).parent
backend_dir = current_dir.parent.parent
academic_research_path = backend_dir / "academic-research"
fomc_research_path = backend_dir / "fomc-research"

# Add paths to sys.path for imports
if academic_research_path.exists():
    sys.path.insert(0, str(academic_research_path))
if fomc_research_path.exists():
    sys.path.insert(0, str(fomc_research_path))

# Import the specialized agents with error handling
AGENTS_AVAILABLE = False
academic_coordinator = None
fomc_agent = None

try:
    from academic_research import academic_coordinator
    print("✅ Successfully imported Academic Research Agent")
except ImportError as e:
    print(f"⚠️  Warning: Could not import Academic Research Agent: {e}")
    print("   This may be due to missing dependencies or authentication issues")

try:
    from fomc_research import root_agent as fomc_agent
    print("✅ Successfully imported FOMC Research Agent")
    print("   Note: BigQuery functionality may not be available without proper credentials")
except ImportError as e:
    print(f"⚠️  Warning: Could not import FOMC Research Agent: {e}")
    print("   This may be due to missing dependencies or authentication issues")
    print("   The FOMC agent requires Google Cloud authentication to be set up")

# Check if both agents are available
if academic_coordinator is not None and fomc_agent is not None:
    AGENTS_AVAILABLE = True
    print("✅ Both specialized agents are available for routing")
elif academic_coordinator is not None:
    print("✅ Academic Research Agent is available for routing")
    print("⚠️  FOMC Research Agent is not available")
elif fomc_agent is not None:
    print("✅ FOMC Research Agent is available for routing")
    print("⚠️  Academic Research Agent is not available")
else:
    print("⚠️  No specialized agents are available")
    print("   The routing agent will still work but with limited functionality")

# Create tools list with available agents
tools = []
if academic_coordinator is not None:
    tools.append(AgentTool(agent=academic_coordinator))
if fomc_agent is not None:
    tools.append(AgentTool(agent=fomc_agent))

routing_agent = LlmAgent(
    name="routing_agent",
    model=MODEL,
    description=(
        "A routing agent that analyzes user requests and directs them to the appropriate "
        "specialized agent - either academic research or FOMC financial analysis."
    ),
    instruction=prompt.ROUTING_AGENT_PROMPT,
    output_key="routed_response",
    tools=tools,
)

root_agent = routing_agent 