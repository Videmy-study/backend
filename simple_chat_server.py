#!/usr/bin/env python3
"""
Simplified Chat Server for testing the Videmy Study Chat API.
This version doesn't require MongoDB or external dependencies.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chat schemas
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message/query")
    user_id: Optional[str] = Field(None, description="Optional user ID for session tracking")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")

class ChatResponse(BaseModel):
    success: bool
    message: str
    response: str = Field(..., description="AI agent's response")
    agent_used: Optional[str] = Field(None, description="Which specialized agent was used")
    routing_reason: Optional[str] = Field(None, description="Why this agent was chosen")
    timestamp: datetime = Field(default_factory=datetime.now)

# Create FastAPI instance
app = FastAPI(
    title="Videmy Study Chat API (Simple)",
    description="Simplified API for testing chat functionality",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class SimpleChatManager:
    """Simple chat manager for testing without external dependencies."""
    
    def __init__(self):
        self.available_agents = ["academic_coordinator", "fomc_research_agent", "political_news_coordinator"]
    
    async def process_chat_message(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a chat message and simulate routing."""
        try:
            message_lower = message.lower()
            
            # Simple keyword-based routing simulation
            if any(keyword in message_lower for keyword in ["research", "paper", "academic", "study", "literature", "citation"]):
                return {
                    "success": True,
                    "message": "Message processed successfully",
                    "response": "I'll route this to our Academic Research Agent. This agent specializes in analyzing research papers, finding related literature, and providing research direction suggestions.",
                    "agent_used": "academic_coordinator",
                    "routing_reason": "Academic research keywords detected"
                }
            elif any(keyword in message_lower for keyword in ["fed", "fomc", "federal reserve", "interest rates", "monetary policy", "financial", "market"]):
                return {
                    "success": True,
                    "message": "Message processed successfully",
                    "response": "I'll route this to our FOMC Research Agent. This agent specializes in analyzing Federal Reserve meetings, financial market implications, and economic policy analysis.",
                    "agent_used": "fomc_research_agent",
                    "routing_reason": "Financial/FOMC keywords detected"
                }
            elif any(keyword in message_lower for keyword in ["political", "news", "government", "election", "policy", "current events"]):
                return {
                    "success": True,
                    "message": "Message processed successfully",
                    "response": "I'll route this to our Political News Agent. This agent specializes in gathering and analyzing political news from multiple sources with bias detection.",
                    "agent_used": "political_news_coordinator",
                    "routing_reason": "Political news keywords detected"
                }
            else:
                return {
                    "success": True,
                    "message": "Message processed successfully",
                    "response": "I can help you with academic research, financial analysis, or political news. Please ask me about any of these topics, and I'll route your query to the appropriate specialized agent.",
                    "agent_used": "routing_agent",
                    "routing_reason": "General inquiry - providing guidance"
                }
                
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return {
                "success": False,
                "message": f"Error processing message: {str(e)}",
                "response": "I encountered an error while processing your request. Please try again.",
                "agent_used": None,
                "routing_reason": "Error occurred"
            }
    
    def get_available_agents(self) -> list:
        """Get list of available specialized agents."""
        return self.available_agents.copy()
    
    def is_available(self) -> bool:
        """Check if the chat service is available."""
        return True

# Create chat manager instance
chat_manager = SimpleChatManager()

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agents(request: ChatRequest):
    """
    Chat with the AI routing agent that directs queries to specialized agents.
    
    This endpoint processes user messages and routes them to the appropriate
    specialized agent (Academic Research, FOMC Research, or Political News)
    based on the content and intent of the message.
    """
    try:
        # Process the chat message through the chat manager
        result = await chat_manager.process_chat_message(
            message=request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        return ChatResponse(
            success=result["success"],
            message=result["message"],
            response=result["response"],
            agent_used=result["agent_used"],
            routing_reason=result["routing_reason"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.get("/chat/agents")
async def get_available_agents():
    """
    Get list of available specialized agents.
    
    Returns information about which AI agents are currently available
    for routing user queries.
    """
    try:
        agents = chat_manager.get_available_agents()
        return {
            "success": True,
            "available_agents": agents,
            "total_agents": len(agents),
            "service_status": "available" if chat_manager.is_available() else "unavailable"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent information: {str(e)}")

@app.get("/chat/health")
async def chat_health_check():
    """
    Health check for the chat service.
    
    Returns the status of the chat manager and routing agent.
    """
    try:
        return {
            "success": True,
            "chat_service": "available" if chat_manager.is_available() else "unavailable",
            "available_agents": len(chat_manager.get_available_agents()),
            "status": "healthy" if chat_manager.is_available() else "unhealthy"
        }
    except Exception as e:
        return {
            "success": False,
            "chat_service": "error",
            "error": str(e),
            "status": "unhealthy"
        }

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Videmy Study Chat API (Simple Version)",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "agents": "/chat/agents", 
            "health": "/chat/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Videmy Study Simple Chat Server...")
    print("📍 Host: 0.0.0.0")
    print("🔌 Port: 8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "simple_chat_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 