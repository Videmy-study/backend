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

"""Tests for the Political News Agent."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from political_news import political_news_coordinator, root_agent
from political_news.sub_agents.news_scraper import scrape_political_news, NewsAPIClient
from political_news.sub_agents.bias_analyzer import analyze_news_bias, BiasAnalyzer


class TestPoliticalNewsAgent:
    """Test the main Political News Agent."""
    
    def test_agent_import(self):
        """Test that the agent can be imported successfully."""
        assert political_news_coordinator is not None
        assert root_agent is not None
        assert political_news_coordinator.name == "political_news_coordinator"
    
    def test_agent_description(self):
        """Test that the agent has the correct description."""
        description = political_news_coordinator.description
        assert "political news" in description.lower()
        assert "unbiased" in description.lower()
        assert "24 hours" in description.lower()
    
    def test_agent_tools(self):
        """Test that the agent has the required tools."""
        tools = political_news_coordinator.tools
        assert len(tools) == 2
        tool_names = [tool.agent.name for tool in tools]
        assert "news_scraper_agent" in tool_names
        assert "bias_analyzer_agent" in tool_names


class TestNewsScraperAgent:
    """Test the News Scraper Sub-Agent."""
    
    def test_news_api_client_initialization(self):
        """Test NewsAPIClient initialization."""
        client = NewsAPIClient()
        assert hasattr(client, 'newsapi_key')
        assert hasattr(client, 'gnews_key')
        assert hasattr(client, 'mediastack_key')
        assert hasattr(client, 'newsdata_key')
    
    @patch('political_news.sub_agents.news_scraper.requests.get')
    def test_get_newsapi_articles_success(self, mock_get):
        """Test successful NewsAPI article retrieval."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "articles": [
                {
                    "title": "Test Political Article",
                    "description": "Test description",
                    "content": "Test content",
                    "url": "https://example.com",
                    "source": {"name": "Test Source"},
                    "publishedAt": datetime.now().isoformat()
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = NewsAPIClient()
        client.newsapi_key = "test_key"
        
        articles = client.get_newsapi_articles("Congress", hours=24)
        
        assert len(articles) == 1
        assert articles[0]["title"] == "Test Political Article"
        assert articles[0]["api_source"] == "NewsAPI"
    
    @patch('political_news.sub_agents.news_scraper.requests.get')
    def test_get_newsapi_articles_no_key(self, mock_get):
        """Test NewsAPI article retrieval without API key."""
        client = NewsAPIClient()
        client.newsapi_key = None
        
        articles = client.get_newsapi_articles("Congress", hours=24)
        
        assert articles == []
        mock_get.assert_not_called()
    
    @patch('political_news.sub_agents.news_scraper.requests.get')
    def test_get_gnews_articles_success(self, mock_get):
        """Test successful GNews article retrieval."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "articles": [
                {
                    "title": "Test GNews Article",
                    "description": "Test description",
                    "content": "Test content",
                    "url": "https://example.com",
                    "source": {"name": "Test Source"},
                    "publishedAt": datetime.now().isoformat()
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = NewsAPIClient()
        client.gnews_key = "test_key"
        
        articles = client.get_gnews_articles("Congress", hours=24)
        
        assert len(articles) == 1
        assert articles[0]["title"] == "Test GNews Article"
        assert articles[0]["api_source"] == "GNews"
    
    @patch('political_news.sub_agents.news_scraper.requests.get')
    def test_get_mediastack_articles_success(self, mock_get):
        """Test successful MediaStack article retrieval."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "title": "Test MediaStack Article",
                    "description": "Test description",
                    "url": "https://example.com",
                    "source": "Test Source",
                    "published_at": datetime.now().isoformat()
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = NewsAPIClient()
        client.mediastack_key = "test_key"
        
        articles = client.get_mediastack_articles("Congress", hours=24)
        
        assert len(articles) == 1
        assert articles[0]["title"] == "Test MediaStack Article"
        assert articles[0]["api_source"] == "MediaStack"
    
    def test_scrape_political_news_integration(self):
        """Test the integrated scraping function."""
        with patch.object(NewsAPIClient, 'get_newsapi_articles', return_value=[]), \
             patch.object(NewsAPIClient, 'get_gnews_articles', return_value=[]), \
             patch.object(NewsAPIClient, 'get_mediastack_articles', return_value=[]):
            
            result = scrape_political_news("Congress", hours=24)
            
            assert result["topic"] == "Congress"
            assert result["time_range_hours"] == 24
            assert result["total_articles"] == 0
            assert isinstance(result["articles"], list)
            assert isinstance(result["sources_used"], list)
            assert "scraped_at" in result


class TestBiasAnalyzerAgent:
    """Test the Bias Analyzer Sub-Agent."""
    
    def test_bias_analyzer_initialization(self):
        """Test BiasAnalyzer initialization."""
        analyzer = BiasAnalyzer()
        assert hasattr(analyzer, 'BIASED_TERMS')
        assert hasattr(analyzer, 'CREDIBLE_SOURCES')
        assert 'left_wing' in analyzer.BIASED_TERMS
        assert 'right_wing' in analyzer.BIASED_TERMS
        assert 'high' in analyzer.CREDIBLE_SOURCES
    
    def test_detect_bias_indicators(self):
        """Test bias indicator detection."""
        analyzer = BiasAnalyzer()
        
        # Test left-wing bias
        text = "The progressive agenda is moving forward with socialist policies"
        indicators = analyzer._detect_bias_indicators(text)
        assert "progressive" in indicators["left_wing_terms"]
        assert "socialist" in indicators["left_wing_terms"]
        
        # Test right-wing bias
        text = "The conservative agenda with America first policies"
        indicators = analyzer._detect_bias_indicators(text)
        assert "conservative agenda" in indicators["right_wing_terms"]
        assert "America first" in indicators["right_wing_terms"]
        
        # Test emotional language
        text = "This is absolutely outrageous and shocking news"
        indicators = analyzer._detect_bias_indicators(text)
        assert "outrageous" in indicators["emotional_terms"]
        assert "shocking" in indicators["emotional_terms"]
    
    def test_assess_source_credibility(self):
        """Test source credibility assessment."""
        analyzer = BiasAnalyzer()
        
        # Test high credibility source
        result = analyzer._assess_source_credibility("Reuters")
        assert result["level"] == "high"
        assert result["score"] == 0.9
        
        # Test medium credibility source
        result = analyzer._assess_source_credibility("Bloomberg")
        assert result["level"] == "medium"
        assert result["score"] == 0.6
        
        # Test unknown source
        result = analyzer._assess_source_credibility("Unknown News Source")
        assert result["level"] == "unknown"
        assert result["score"] == 0.5
    
    def test_detect_emotional_language(self):
        """Test emotional language detection."""
        analyzer = BiasAnalyzer()
        
        # Test with emotional language
        text = "This is absolutely outrageous and shocking news that is devastating"
        score = analyzer._detect_emotional_language(text)
        assert score > 0
        
        # Test without emotional language
        text = "The government announced new policies today"
        score = analyzer._detect_emotional_language(text)
        assert score == 0.0
    
    def test_detect_partisan_language(self):
        """Test partisan language detection."""
        analyzer = BiasAnalyzer()
        
        # Test with partisan language
        text = "Democrats say this while Republicans claim that"
        score = analyzer._detect_partisan_language(text)
        assert score > 0
        
        # Test without partisan language
        text = "The government announced new policies today"
        score = analyzer._detect_partisan_language(text)
        assert score == 0.0
    
    def test_calculate_bias_score(self):
        """Test bias score calculation."""
        analyzer = BiasAnalyzer()
        
        # Test with high credibility and low bias
        bias_indicators = {
            "left_wing_terms": [],
            "right_wing_terms": [],
            "emotional_terms": [],
            "partisan_terms": [],
            "loaded_language": [],
            "factual_claims": ["according to", "data shows"],
            "opinion_indicators": []
        }
        credibility_score = {"score": 0.9}
        emotional_score = 0.0
        partisan_score = 0.0
        
        score = analyzer._calculate_bias_score(
            bias_indicators, credibility_score, emotional_score, partisan_score
        )
        assert score >= 0.8  # Should be high score for low bias
    
    def test_categorize_bias(self):
        """Test bias categorization."""
        analyzer = BiasAnalyzer()
        
        assert "Low Bias" in analyzer._categorize_bias(0.9)
        assert "Moderate Bias" in analyzer._categorize_bias(0.7)
        assert "High Bias" in analyzer._categorize_bias(0.5)
        assert "Very High Bias" in analyzer._categorize_bias(0.3)
    
    def test_analyze_article_bias(self):
        """Test complete article bias analysis."""
        analyzer = BiasAnalyzer()
        
        article = {
            "title": "Congress Passes New Bill",
            "description": "The government announced new policies today",
            "content": "According to official sources, the new legislation was approved",
            "source": "Reuters"
        }
        
        analysis = analyzer.analyze_article_bias(article)
        
        assert "article_title" in analysis
        assert "source" in analysis
        assert "bias_indicators" in analysis
        assert "credibility_score" in analysis
        assert "overall_bias_score" in analysis
        assert "bias_category" in analysis
        assert "recommendations" in analysis
        assert analysis["source"] == "Reuters"
    
    def test_analyze_news_bias_integration(self):
        """Test the integrated bias analysis function."""
        articles = [
            {
                "title": "Congress Passes New Bill",
                "description": "The government announced new policies today",
                "content": "According to official sources, the new legislation was approved",
                "source": "Reuters"
            },
            {
                "title": "Another Political Story",
                "description": "More political news",
                "content": "Additional political content",
                "source": "AP"
            }
        ]
        
        result = analyze_news_bias(articles)
        
        assert result["total_articles_analyzed"] == 2
        assert "average_bias_score" in result
        assert "bias_distribution" in result
        assert "overall_recommendations" in result
        assert "individual_analyses" in result
        assert len(result["individual_analyses"]) == 2


class TestAgentIntegration:
    """Test integration between agents."""
    
    def test_agent_tool_connections(self):
        """Test that agents are properly connected as tools."""
        # Check that the coordinator has the sub-agents as tools
        tools = political_news_coordinator.tools
        tool_agents = [tool.agent for tool in tools]
        
        # Find the news scraper and bias analyzer agents
        news_scraper = next((agent for agent in tool_agents if agent.name == "news_scraper_agent"), None)
        bias_analyzer = next((agent for agent in tool_agents if agent.name == "bias_analyzer_agent"), None)
        
        assert news_scraper is not None
        assert bias_analyzer is not None
        assert news_scraper.name == "news_scraper_agent"
        assert bias_analyzer.name == "bias_analyzer_agent"
    
    def test_agent_prompts(self):
        """Test that agents have proper prompts."""
        assert political_news_coordinator.instruction is not None
        assert len(political_news_coordinator.instruction) > 0
        
        # Check that the prompt contains key elements
        prompt = political_news_coordinator.instruction
        assert "political news" in prompt.lower()
        assert "unbiased" in prompt.lower()
        assert "24 hours" in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__]) 