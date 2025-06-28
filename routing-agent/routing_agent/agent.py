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
project_root = current_dir.parent.parent
academic_research_path = project_root / "academic-research"
fomc_research_path = project_root / "fomc-research"

# Add paths to sys.path for imports
if academic_research_path.exists():
    sys.path.insert(0, str(academic_research_path))
if fomc_research_path.exists():
    sys.path.insert(0, str(fomc_research_path))

# Import the specialized agents
try:
    from academic_research.academic_research.agent import academic_coordinator
    from fomc_research.fomc_research.agent import root_agent as fomc_agent
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import specialized agents: {e}")
    print("Please ensure academic-research and fomc-research agents are available")
    AGENTS_AVAILABLE = False

routing_agent = LlmAgent(
    name="routing_agent",
    model=MODEL,
    description=(
        "A routing agent that analyzes user requests and directs them to the appropriate "
        "specialized agent - either academic research or FOMC financial analysis."
    ),
    instruction=prompt.ROUTING_AGENT_PROMPT,
    output_key="routed_response",
    tools=[
        AgentTool(agent=academic_coordinator) if AGENTS_AVAILABLE else None,
        AgentTool(agent=fomc_agent) if AGENTS_AVAILABLE else None,
    ] if AGENTS_AVAILABLE else [],
)

root_agent = routing_agent 