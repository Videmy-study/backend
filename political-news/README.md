# Political News Agent

A sophisticated multi-agent system that scrapes and analyzes unbiased political news from the last 24 hours using multiple news APIs.

## Overview

The Political News Agent is designed to provide comprehensive, unbiased political news coverage by:

- **Multi-Source News Gathering**: Uses NewsAPI, GNews, MediaStack, and other APIs
- **Bias Analysis**: Analyzes articles for political bias, emotional language, and credibility
- **Time-Based Filtering**: Focuses on news from the last 24 hours
- **Source Diversity**: Ensures balanced coverage from multiple perspectives
- **Credibility Assessment**: Evaluates source reliability and provides recommendations

## Architecture

The agent consists of three main components:

### 1. Political News Coordinator (Root Agent)
- Orchestrates the news gathering and analysis process
- Coordinates between news scraping and bias analysis sub-agents
- Provides comprehensive summaries and recommendations

### 2. News Scraper Sub-Agent
- Gathers articles from multiple news APIs
- Filters for political relevance and recency
- Deduplicates articles and ensures source diversity
- Supports NewsAPI, GNews, MediaStack, and NewsData.io

### 3. Bias Analyzer Sub-Agent
- Analyzes articles for political bias and credibility
- Detects emotional language and partisan framing
- Assesses source reliability
- Provides specific recommendations for using information

## Features

### News Gathering Capabilities
- **Multi-API Integration**: NewsAPI, GNews, MediaStack, NewsData.io
- **Political Focus**: Filters for government, congress, senate, presidential activities
- **Time Filtering**: Prioritizes articles from the last 24 hours
- **Source Diversity**: Includes mainstream and specialized political news outlets
- **Deduplication**: Removes duplicate articles while maintaining diversity

### Bias Analysis Features
- **Political Bias Detection**: Identifies left-wing and right-wing language
- **Emotional Language Analysis**: Detects sensationalist and loaded terms
- **Source Credibility Assessment**: Evaluates known and unknown sources
- **Fact vs Opinion Distinction**: Separates factual claims from opinions
- **Comprehensive Scoring**: Provides 0-1 bias scores with categories

### Trusted News Sources
- **High Credibility**: Reuters, AP, BBC News, NPR, PBS, C-SPAN, major newspapers
- **Medium Credibility**: Bloomberg, Forbes, Time, Newsweek, The Atlantic
- **Low Credibility**: Known biased outlets (identified for transparency)

## Installation

### Prerequisites
- Python 3.9 or higher
- Poetry (for dependency management)

### Setup

1. **Clone the repository**:
   ```bash
   cd backend/political-news
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file with your API keys
   cp .env.example .env
   ```

4. **Configure API keys**:
   ```bash
   # Add your news API keys to .env
   NEWSAPI_KEY=your_newsapi_key
   GNEWS_API_KEY=your_gnews_key
   MEDIASTACK_API_KEY=your_mediastack_key
   NEWSDATA_API_KEY=your_newsdata_key
   ```

## API Keys Required

### NewsAPI.org
- **URL**: https://newsapi.org/
- **Free Tier**: 1,000 requests/day
- **Features**: Comprehensive news aggregation with political filtering

### GNews API
- **URL**: https://gnews.io/
- **Free Tier**: 100 requests/day
- **Features**: Google News alternative with real-time updates

### MediaStack
- **URL**: https://mediastack.com/
- **Free Tier**: 500 requests/month
- **Features**: Global news coverage with extensive source network

### NewsData.io
- **URL**: https://newsdata.io/
- **Free Tier**: 200 requests/day
- **Features**: Additional news source for comprehensive coverage

## Usage

### Basic Usage

```python
from political_news import political_news_coordinator

# Analyze political news about a specific topic
response = political_news_coordinator.run(
    "What happened in Congress yesterday?"
)

print(response.news_analysis)
```

### Advanced Usage

```python
from political_news.sub_agents.news_scraper import scrape_political_news
from political_news.sub_agents.bias_analyzer import analyze_news_bias

# Scrape news articles
news_data = scrape_political_news("Supreme Court", hours=24)

# Analyze bias
bias_analysis = analyze_news_bias(news_data["articles"])

print(f"Found {news_data['total_articles']} articles")
print(f"Average bias score: {bias_analysis['average_bias_score']}")
```

### Example Queries

- "What happened in Congress yesterday?"
- "Tell me about the latest Supreme Court decision"
- "What's the latest on the presidential campaign?"
- "Get news about federal policy changes"
- "Find articles about state political developments"

## Output Format

### News Analysis Response
```json
{
  "executive_summary": "Key political developments from the last 24 hours",
  "detailed_analysis": "In-depth coverage of major events",
  "multiple_perspectives": "Different viewpoints on controversial topics",
  "source_credibility": "Assessment of information reliability",
  "implications": "Potential impact of political developments",
  "recommendations": "Guidance for further research"
}
```

### Bias Analysis Response
```json
{
  "total_articles_analyzed": 15,
  "average_bias_score": 0.72,
  "bias_distribution": {
    "Low Bias": 8,
    "Moderate Bias": 5,
    "High Bias": 2,
    "Very High Bias": 0
  },
  "overall_recommendations": [
    "Most articles appear credible and balanced"
  ],
  "individual_analyses": [...],
  "analysis_summary": {
    "most_credible_sources": ["Reuters", "AP", "BBC News"],
    "least_credible_sources": ["Unknown Source"],
    "common_bias_indicators": {...}
  }
}
```

## Testing

Run the test suite:

```bash
poetry run pytest
```

Run specific tests:

```bash
poetry run pytest tests/test_news_scraper.py
poetry run pytest tests/test_bias_analyzer.py
```

## Configuration

### Environment Variables

```bash
# News API Keys
NEWSAPI_KEY=your_newsapi_key
GNEWS_API_KEY=your_gnews_key
MEDIASTACK_API_KEY=your_mediastack_key
NEWSDATA_API_KEY=your_newsdata_key

# Google ADK Configuration
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_API_KEY=your_gemini_api_key
```

### Customization

You can customize the agent behavior by modifying:

- **Bias Detection**: Add new biased terms in `bias_analyzer.py`
- **Source Credibility**: Update source lists in `bias_analyzer.py`
- **API Configuration**: Modify API parameters in `news_scraper.py`
- **Time Filtering**: Adjust the default 24-hour window

## Error Handling

The agent includes robust error handling:

- **API Failures**: Gracefully handles API outages and rate limits
- **Missing Keys**: Continues with available APIs when some keys are missing
- **Network Issues**: Implements timeouts and retry logic
- **Data Validation**: Validates article data before processing

## Limitations

- **API Rate Limits**: Free tiers have daily/monthly request limits
- **Source Availability**: Some sources may not be available in all APIs
- **Bias Detection**: Automated bias detection is not perfect and should be used as guidance
- **Content Access**: Some articles may require subscriptions or have paywalls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0.

## Support

For questions or issues:

1. Check the documentation
2. Review the test examples
3. Open an issue on GitHub
4. Contact the development team

## Roadmap

- [ ] Add more news APIs (NewsData.io integration)
- [ ] Implement article content extraction
- [ ] Add sentiment analysis
- [ ] Create web interface
- [ ] Add historical news analysis
- [ ] Implement news alerts and notifications
- [ ] Add multilingual support
- [ ] Create news summarization features 