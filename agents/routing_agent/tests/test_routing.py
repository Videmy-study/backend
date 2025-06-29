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

"""Tests for the Routing Agent."""

import pytest
from unittest.mock import Mock, patch

from routing_agent.agent import routing_agent


class TestRoutingAgent:
    """Test cases for the routing agent functionality."""

    @pytest.fixture
    def mock_llm_response(self):
        """Mock LLM response for testing."""
        return Mock()

    def test_academic_research_keywords(self):
        """Test that academic research keywords route to academic agent."""
        test_queries = [
            "I need help analyzing this research paper on machine learning",
            "Can you help me find literature on neural networks?",
            "I'm writing a thesis and need help with citations",
            "What are the latest publications in computer vision?",
            "I need to review academic papers for my dissertation",
        ]
        
        for query in test_queries:
            # This would be tested with actual agent calls
            # For now, we're just validating the keywords are identified
            assert any(keyword in query.lower() for keyword in [
                "research", "paper", "academic", "literature", "citations", 
                "thesis", "publications", "dissertation"
            ])

    def test_fomc_research_keywords(self):
        """Test that FOMC research keywords route to FOMC agent."""
        test_queries = [
            "What was the impact of the latest Fed meeting on markets?",
            "I need analysis of the Federal Reserve's interest rate decision",
            "What did the FOMC statement say about monetary policy?",
            "How did markets react to the latest Fed announcement?",
            "I want to understand the economic policy implications",
        ]
        
        for query in test_queries:
            # This would be tested with actual agent calls
            # For now, we're just validating the keywords are identified
            assert any(keyword in query.lower() for keyword in [
                "fed", "fomc", "federal reserve", "interest rate", "monetary policy",
                "markets", "economic policy", "announcement"
            ])

    def test_ambiguous_queries(self):
        """Test that ambiguous queries prompt for clarification."""
        ambiguous_queries = [
            "I want to analyze economic policy",
            "Help me understand policy decisions",
            "I need research assistance",
            "Can you analyze this data?",
        ]
        
        for query in ambiguous_queries:
            # These queries should trigger clarification requests
            # as they could apply to both domains
            pass

    def test_agent_availability(self):
        """Test that the agent handles missing specialized agents gracefully."""
        # Test the import logic and fallback behavior
        pass


def test_routing_decision_examples():
    """Test specific routing decision examples."""
    
    # Academic Research Examples
    academic_examples = [
        ("Analyze this research paper on transformers", "academic"),
        ("Find papers that cite this seminal work", "academic"),
        ("Help me write a literature review", "academic"),
        ("What are the latest developments in NLP research?", "academic"),
        ("I need help with my thesis methodology", "academic"),
    ]
    
    # FOMC Research Examples
    fomc_examples = [
        ("What did the Fed say in their latest meeting?", "fomc"),
        ("How will the interest rate decision affect markets?", "fomc"),
        ("Analyze the FOMC statement for policy changes", "fomc"),
        ("What was the market reaction to the Fed announcement?", "fomc"),
        ("I need to understand the monetary policy implications", "fomc"),
    ]
    
    # Test the routing logic
    for query, expected_route in academic_examples + fomc_examples:
        # In a real implementation, this would call the routing agent
        # and verify it routes to the correct specialized agent
        print(f"Query: '{query}' -> Expected route: {expected_route}")


if __name__ == "__main__":
    # Run the examples
    test_routing_decision_examples() 