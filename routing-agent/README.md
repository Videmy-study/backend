# Routing Agent

A smart routing agent that analyzes user requests and directs them to the appropriate specialized agent - Academic Research Agent, FOMC Research Agent, or Political News Agent.

## Overview

The Routing Agent serves as an intelligent dispatcher that:

1. **Analyzes user requests** to understand the primary topic and intent
2. **Identifies key indicators** that suggest which specialized agent would be most appropriate
3. **Routes requests** to the appropriate agent using Google's Agent Development Kit (ADK)
4. **Provides context** to the specialized agent about why they were chosen

## Agent Details

| Feature | Description |
| --- | --- |
| **Interaction Type** | Conversational |
| **Complexity** | Medium |
| **Agent Type** | Multi Agent |
| **Components** | Agent Tools |
| **Vertical** | General Purpose |

## Available Specialized Agents

### Academic Research Agent
- **Purpose**: Academic research, literature analysis, and research direction suggestions
- **Keywords**: papers, research, academic, literature, citations, scholarly, university, thesis, dissertation, publication, journal, conference, methodology, references

### FOMC Research Agent
- **Purpose**: Federal Open Market Committee meetings and financial market analysis
- **Keywords**: Fed, FOMC, Federal Reserve, interest rates, monetary policy, financial markets, economic policy, banking, market analysis, rate decisions, economic indicators, financial services

### Political News Agent
- **Purpose**: Scrapes and analyzes unbiased political news from multiple sources
- **Keywords**: political news, current events, government, elections, policy, politics, political analysis, news, current affairs, political developments, government decisions, political campaigns, legislative, voting, political opinion

## Setup and Installation

### Prerequisites

- Python 3.11+
- Poetry for dependency management
- Google Cloud Platform project
- Google Cloud CLI

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd routing-agent
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Configure Google Cloud credentials**:
   ```bash
   export GOOGLE_GENAI_USE_VERTEXAI=true
   export GOOGLE_CLOUD_PROJECT=<your-project-id>
   export GOOGLE_CLOUD_LOCATION=<your-project-location>
   ```

4. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth application-default login
   gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
   ```

## Configuration

### Agent Integration

To integrate with the existing academic-research, fomc-research, and political-news agents, you need to:

1. **Update the import paths** in `routing_agent/agent.py`:
   ```python
   # Uncomment and adjust these imports based on your project structure
   from academic_research.academic_research.agent import academic_coordinator
   from fomc_research.fomc_research.agent import root_agent as fomc_agent
   from political_news.political_news.agent import political_news_coordinator
   ```

2. **Add the agents to the tools list**:
   ```python
   tools=[
       AgentTool(agent=academic_coordinator),
       AgentTool(agent=fomc_agent),
       AgentTool(agent=political_news_coordinator),
   ],
   ```

### Project Structure

Ensure your project structure looks like this:
```
your-project/
├── routing-agent/
│   ├── routing_agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   ├── pyproject.toml
│   └── README.md
├── academic-research/
│   └── academic_research/
│       └── agent.py
├── fomc-research/
│   └── fomc_research/
│       └── agent.py
└── political-news/
    └── political_news/
        └── agent.py
```

## Running the Agent

### Using ADK CLI

```bash
adk run routing_agent
```

### Using ADK Web Interface

```bash
adk web
```

Then select "routing_agent" from the dropdown menu.

## Example Interactions

### Academic Research Request
```
User: "I need help analyzing this research paper on machine learning"

Routing Agent: I'll route this to the Academic Research Agent since you're asking about analyzing a research paper. This agent specializes in academic literature analysis and can help you understand the paper's contributions, find related research, and suggest future directions.

[Routes to Academic Research Agent]
```

### FOMC Research Request
```
User: "What was the impact of the latest Fed meeting on markets?"

Routing Agent: I'll route this to the FOMC Research Agent since you're asking about Federal Reserve meetings and market impact. This agent specializes in analyzing FOMC meetings, statements, and their financial market implications.

[Routes to FOMC Research Agent]
```

### Political News Request
```
User: "What's the latest news on the Israel-Palestine conflict?"

Routing Agent: I'll route this to the Political News Agent since you're asking about current political news and events. This agent specializes in gathering and analyzing political news from multiple sources, providing unbiased coverage of current political developments.

[Routes to Political News Agent]
```

### Ambiguous Request
```
User: "I want to analyze economic policy"

Routing Agent: I need to clarify what type of economic policy analysis you're looking for. Are you:
1. Analyzing academic research papers about economic policy (Academic Research Agent)
2. Analyzing current Federal Reserve policy decisions and their market impact (FOMC Research Agent)
3. Looking for current news about economic policy changes (Political News Agent)

Please provide more context so I can route you to the most appropriate agent.
```

## Decision Framework

The routing agent uses the following logic:

1. **Keyword Analysis**: Identifies domain-specific keywords in the user's request
2. **Intent Classification**: Determines whether the request is primarily academic, financial, or political
3. **Context Assessment**: Considers the broader context and user's likely goals
4. **Clarification**: Asks for clarification when the intent is ambiguous

## Customization

### Adding New Specialized Agents

To add new specialized agents:

1. **Create the new agent** following the ADK pattern
2. **Update the prompt** in `prompt.py` to include the new agent's capabilities
3. **Add the agent tool** to the tools list in `agent.py`
4. **Update the decision framework** in the prompt

### Modifying Routing Logic

Edit the `ROUTING_AGENT_PROMPT` in `prompt.py` to:
- Add new keywords and indicators
- Modify the decision framework
- Include additional examples
- Adjust the response format

## Deployment

### Local Development

```bash
poetry install
adk run routing_agent
```

### Production Deployment

Follow the [Google Agent Engine deployment guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up) for production deployment.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the specialized agents are properly installed and importable
2. **Authentication Issues**: Verify Google Cloud credentials are properly configured
3. **Routing Confusion**: Review and refine the prompt keywords and decision logic

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
adk run routing_agent
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0. 