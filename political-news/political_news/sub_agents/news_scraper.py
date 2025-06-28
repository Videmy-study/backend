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

"""News Scraper Sub-Agent: Gathers political news from multiple APIs."""

import logging
import os
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import news_scraper_prompt

MODEL = "gemini-2.5-pro"

logger = logging.getLogger(__name__)

class NewsAPIClient:
    """Client for various news APIs."""
    
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.gnews_key = os.getenv("GNEWS_API_KEY")
        self.mediastack_key = os.getenv("MEDIASTACK_API_KEY")
        self.newsdata_key = os.getenv("NEWSDATA_API_KEY")
        
    def get_newsapi_articles(self, topic: str) -> List[Dict[str, Any]]:
        """Get articles from NewsAPI.org."""
        if not self.newsapi_key:
            logger.warning("NEWSAPI_KEY not found in environment variables")
            return []
            
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": f"{topic}",  # Simplified query for better results
                "language": "en",
                "sortBy": "publishedAt",
                "apiKey": self.newsapi_key,
                "pageSize": 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # Handle rate limiting gracefully
            if response.status_code == 429:
                logger.warning("NewsAPI rate limit reached, skipping this source")
                return []
            elif response.status_code != 200:
                logger.error(f"NewsAPI error {response.status_code}: {response.text[:100]}")
                return []
            
            data = response.json()
            articles = data.get("articles", [])
            
            # Process all articles without time filtering
            processed_articles = []
            
            for article in articles:
                try:
                    processed_articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "content": article.get("content", ""),
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "publishedAt": article.get("publishedAt", ""),
                        "api_source": "NewsAPI"
                    })
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping article due to parsing error: {e}")
                    continue
            
            return processed_articles
            
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def get_gnews_articles(self, topic: str) -> List[Dict[str, Any]]:
        """Get articles from GNews API."""
        if not self.gnews_key:
            logger.warning("GNEWS_API_KEY not found in environment variables")
            return []
            
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": f"{topic}",  # Simplified query for better results
                "lang": "en",
                "country": "us",
                "max": 20,
                "apikey": self.gnews_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # Handle rate limiting gracefully
            if response.status_code == 429:
                logger.warning("GNews rate limit reached, skipping this source")
                return []
            elif response.status_code != 200:
                logger.error(f"GNews error {response.status_code}: {response.text[:100]}")
                return []
            
            data = response.json()
            articles = data.get("articles", [])
            
            # Process all articles without time filtering
            processed_articles = []
            
            for article in articles:
                try:
                    processed_articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "content": article.get("content", ""),
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "publishedAt": article.get("publishedAt", ""),
                        "api_source": "GNews"
                    })
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping article due to parsing error: {e}")
                    continue
            
            return processed_articles
            
        except Exception as e:
            logger.error(f"Error fetching from GNews: {e}")
            return []
    
    def get_mediastack_articles(self, topic: str) -> List[Dict[str, Any]]:
        """Get articles from MediaStack API."""
        if not self.mediastack_key:
            logger.warning("MEDIASTACK_API_KEY not found in environment variables")
            return []
            
        try:
            url = "http://api.mediastack.com/v1/news"
            params = {
                "access_key": self.mediastack_key,
                "keywords": f"{topic}",  # Simplified query for better results
                "languages": "en",
                "countries": "us",
                "limit": 20,
                "sort": "published_desc"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # Handle rate limiting gracefully
            if response.status_code == 429:
                logger.warning("MediaStack rate limit reached, skipping this source")
                return []
            elif response.status_code != 200:
                logger.error(f"MediaStack error {response.status_code}: {response.text[:100]}")
                return []
            
            data = response.json()
            articles = data.get("data", [])
            
            # Process all articles without time filtering
            processed_articles = []
            
            for article in articles:
                try:
                    processed_articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "content": "",  # MediaStack doesn't provide content
                        "url": article.get("url", ""),
                        "source": article.get("source", ""),
                        "publishedAt": article.get("published_at", ""),
                        "api_source": "MediaStack"
                    })
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping article due to parsing error: {e}")
                    continue
            
            return processed_articles
            
        except Exception as e:
            logger.error(f"Error fetching from MediaStack: {e}")
            return []

def scrape_political_news(request: str, hours: int = None) -> Dict[str, Any]:
    """Scrape political news from multiple APIs for a given request."""
    client = NewsAPIClient()
    
    # Gather articles from multiple sources (no time limit)
    newsapi_articles = client.get_newsapi_articles(request)
    gnews_articles = client.get_gnews_articles(request)
    mediastack_articles = client.get_mediastack_articles(request)
    
    # Combine and deduplicate articles
    all_articles = newsapi_articles + gnews_articles + mediastack_articles
    
    # Simple deduplication based on title similarity
    seen_titles = set()
    unique_articles = []
    
    for article in all_articles:
        title_lower = article["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_articles.append(article)
    
    # Sort by publication date (newest first)
    unique_articles.sort(key=lambda x: x["publishedAt"], reverse=True)
    
    return {
        "topic": request,
        "time_range": "No time limit - all available articles",
        "total_articles": len(unique_articles),
        "articles": unique_articles,
        "sources_used": list(set(article["api_source"] for article in unique_articles)),
        "scraped_at": datetime.now(timezone.utc).isoformat()
    }

news_scraper_agent = LlmAgent(
    name="news_scraper_agent",
    model=MODEL,
    description=(
        "Scrapes political news articles from multiple APIs including NewsAPI, "
        "GNews, and MediaStack. Focuses on the last 24 hours and filters for "
        "political relevance."
    ),
    instruction=news_scraper_prompt.NEWS_SCRAPER_PROMPT,
    output_key="scraped_news",
    tools=[scrape_political_news],
) 