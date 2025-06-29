import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ChatManager:
    """Manages chat interactions with the routing agent and specialized agents."""
    
    def __init__(self):
        self.routing_agent = None
        self.available_agents = ["academic_coordinator", "fomc_research_agent", "political_news_coordinator"]
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize the routing agent and check available specialized agents."""
        try:
            # Try to import the routing agent if available
            current_dir = Path(__file__).parent.parent
            agents_dir = current_dir / "agents"
            routing_agent_dir = agents_dir / "routing-agent"
            
            if routing_agent_dir.exists():
                # Add the routing agent directory to the path
                sys.path.insert(0, str(routing_agent_dir))
                
                try:
                    from routing_agent.routing_agent.agent import routing_agent, AGENTS_AVAILABLE
                    self.routing_agent = routing_agent
                    logger.info("Routing agent initialized successfully")
                except ImportError as e:
                    logger.warning(f"Could not import routing agent: {e}")
                    logger.info("Running in simulation mode")
                    self.routing_agent = None
            else:
                logger.info("Routing agent directory not found, running in simulation mode")
                self.routing_agent = None
                
        except Exception as e:
            logger.error(f"Error initializing chat manager: {e}")
            self.routing_agent = None
    
    async def process_chat_message(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a chat message and route it to the appropriate specialized agent.
        
        Args:
            message: The user's message/query
            user_id: Optional user ID for session tracking
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # For now, we'll simulate the routing process
            response_data = await self._simulate_routing(message, {
                "user_query": message,
                "user_id": user_id or "anonymous",
                "session_id": session_id or "default"
            })
            
            return {
                "success": True,
                "message": "Message processed successfully",
                "response": response_data.get("response", "I'm here to help! Please ask me about academic research, financial analysis, or political news."),
                "agent_used": response_data.get("agent_used", "routing_agent"),
                "routing_reason": response_data.get("routing_reason", "General routing")
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
    
    async def _simulate_routing(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate the routing process until the actual routing agent is fully integrated.
        
        Args:
            message: The user's message
            context: Context information
            
        Returns:
            Simulated response data
        """
        message_lower = message.lower()
        
        # Simple keyword-based routing simulation
        if any(keyword in message_lower for keyword in ["research", "paper", "academic", "study", "literature", "citation"]):
            return {
                "response": "I'll route this to our Academic Research Agent. This agent specializes in analyzing research papers, finding related literature, and providing research direction suggestions.",
                "agent_used": "academic_coordinator",
                "routing_reason": "Academic research keywords detected"
            }
        elif any(keyword in message_lower for keyword in ["fed", "fomc", "federal reserve", "interest rates", "monetary policy", "financial", "market"]):
            return {
                "response": "I'll route this to our FOMC Research Agent. This agent specializes in analyzing Federal Reserve meetings, financial market implications, and economic policy analysis.",
                "agent_used": "fomc_research_agent",
                "routing_reason": "Financial/FOMC keywords detected"
            }
        elif any(keyword in message_lower for keyword in ["political", "news", "government", "election", "policy", "current events"]):
            return {
                "response": "I'll route this to our Political News Agent. This agent specializes in gathering and analyzing political news from multiple sources with bias detection.",
                "agent_used": "political_news_coordinator",
                "routing_reason": "Political news keywords detected"
            }
        else:
            return {
                "response": "I can help you with academic research, financial analysis, or political news. Please ask me about any of these topics, and I'll route your query to the appropriate specialized agent.",
                "agent_used": "routing_agent",
                "routing_reason": "General inquiry - providing guidance"
            }
    
    def get_available_agents(self) -> list:
        """Get list of available specialized agents."""
        return self.available_agents.copy()
    
    def is_available(self) -> bool:
        """Check if the chat service is available."""
        return True  # Always available in simulation mode

# Create a global instance
chat_manager = ChatManager() 