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

"""Political News Agent: Scrapes unbiased political news from the last 24 hours."""

import logging
import os
from datetime import datetime, timedelta

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.news_scraper import news_scraper_agent
from .sub_agents.bias_analyzer import bias_analyzer_agent

MODEL = "gemini-2.5-pro"

logger = logging.getLogger(__name__)

political_news_coordinator = LlmAgent(
    name="political_news_coordinator",
    model=MODEL,
    description=(
        "Scrapes and analyzes unbiased political news from the last 24 hours. "
        "Uses multiple news APIs to gather articles on specific topics, "
        "analyzes them for bias, and provides comprehensive summaries."
    ),
    instruction=prompt.POLITICAL_NEWS_COORDINATOR_PROMPT,
    output_key="news_analysis",
    tools=[
        AgentTool(agent=news_scraper_agent),
        AgentTool(agent=bias_analyzer_agent),
    ],
)

root_agent = political_news_coordinator 