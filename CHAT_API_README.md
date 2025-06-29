# Videmy Study Chat API

This document describes the chat API endpoints for the Videmy Study platform, which provides intelligent routing to specialized AI agents.

## Overview

The chat API allows users to interact with the Videmy Study platform through natural language queries. The system automatically routes queries to the appropriate specialized agent based on the content and intent of the message.

## Available Agents

1. **Academic Research Agent** - Handles academic papers, research analysis, and literature reviews
2. **FOMC Research Agent** - Analyzes Federal Reserve meetings and financial market implications
3. **Political News Agent** - Gathers and analyzes political news from multiple sources

## API Endpoints

### 1. Chat with Agents

**Endpoint:** `POST /chat`

**Description:** Send a message and get a response from the appropriate specialized agent.

**Request Body:**
```json
{
  "message": "I need help analyzing a research paper on machine learning",
  "user_id": "optional_user_id",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Message processed successfully",
  "response": "I'll route this to our Academic Research Agent...",
  "agent_used": "academic_coordinator",
  "routing_reason": "Academic research keywords detected",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Get Available Agents

**Endpoint:** `GET /chat/agents`

**Description:** Get information about available specialized agents.

**Response:**
```json
{
  "success": true,
  "available_agents": ["academic_coordinator", "fomc_research_agent", "political_news_coordinator"],
  "total_agents": 3,
  "service_status": "available"
}
```

### 3. Chat Health Check

**Endpoint:** `GET /chat/health`

**Description:** Check the health status of the chat service.

**Response:**
```json
{
  "success": true,
  "chat_service": "available",
  "available_agents": 3,
  "status": "healthy"
}
```

## Example Usage

### Academic Research Query
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need help analyzing this research paper on machine learning",
    "user_id": "user123"
  }'
```

### Financial Analysis Query
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What was the impact of the latest Fed meeting on markets?",
    "user_id": "user123"
  }'
```

### Political News Query
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the latest news on the Israel-Palestine conflict?",
    "user_id": "user123"
  }'
```

## Running the Server

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the server:**
   ```bash
   python start_server.py
   ```

4. **Test the API:**
   ```bash
   python test_chat_api.py
   ```

## Testing

Use the provided test script to verify all endpoints:

```bash
python test_chat_api.py
```

The test script will:
- Check the health of the chat service
- List available agents
- Test routing with different types of queries
- Display routing decisions and agent usage

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad request (invalid input)
- `500` - Internal server error

Error responses include:
```json
{
  "success": false,
  "error": "Error description",
  "details": "Additional error details"
}
```

## Architecture

The chat API uses a layered architecture:

1. **FastAPI Application** - Handles HTTP requests and responses
2. **Chat Manager** - Manages chat interactions and routing logic
3. **Routing Agent** - Determines which specialized agent to use
4. **Specialized Agents** - Process specific types of queries

## Configuration

Key environment variables:

- `GOOGLE_API_KEY` - Google Gemini API key
- `MONGODB_URI` - MongoDB connection string
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

## Development

To extend the chat functionality:

1. Add new specialized agents in the `agents/` directory
2. Update the routing logic in `managers/chat_manager.py`
3. Add new schemas in `api/schemas.py`
4. Update tests in `test_chat_api.py` 