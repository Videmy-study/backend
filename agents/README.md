# Agents Directory

This directory contains all the specialized AI agents for the GDG Solution Hacks project.

## Structure

```
agents/
├── academic-research/     # Academic research and paper analysis agent
├── fomc-research/         # FOMC meeting analysis and financial research agent
├── political-news/        # Political news scraping and analysis agent
└── routing-agent/         # Main routing agent (to be moved here)
```

## Agents Overview

### Academic Research Agent
- **Purpose**: Analyzes academic papers, provides research advice, and suggests new research directions
- **Capabilities**: Web search, paper analysis, research recommendations
- **Dependencies**: google-adk, google-genai, pydantic

### FOMC Research Agent
- **Purpose**: Analyzes Federal Open Market Committee meetings and financial data
- **Capabilities**: BigQuery integration, financial analysis, meeting summaries
- **Dependencies**: google-cloud-bigquery, scikit-learn, pdfplumber, tabulate

### Political News Agent
- **Purpose**: Scrapes and analyzes political news from multiple sources
- **Capabilities**: News aggregation, bias analysis, 24-hour news monitoring
- **Dependencies**: requests, python-dotenv, deprecated

### Routing Agent
- **Purpose**: Routes user requests to the appropriate specialized agent
- **Capabilities**: Request analysis, agent selection, response coordination
- **Dependencies**: google-adk, python-dotenv

## Usage

All agents are designed to work from the unified backend environment. To use them:

1. Activate the backend virtual environment:
   ```powershell
   cd backend
   .\.venv\Scripts\Activate.ps1
   ```

2. Run the routing agent (recommended):
   ```powershell
   cd agents/routing-agent
   adk run routing_agent
   ```

3. Or run individual agents directly:
   ```powershell
   cd agents/academic-research
   adk run academic_research
   
   cd agents/fomc-research
   adk run fomc_research
   
   cd agents/political-news
   adk run political_news
   ```

## Environment Setup

Each agent may require specific environment variables. Check the individual agent directories for `.env-example` files and configure as needed.

## Dependencies

All dependencies are managed centrally in `backend/requirements.txt`. The unified environment ensures all agents can access their required packages. 