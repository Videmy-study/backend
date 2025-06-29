import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

async def get_first_asyncgen_result(asyncgen):
    async for item in asyncgen:
        return item
    return None

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
            routing_agent_dir = agents_dir / "routing_agent"
            
            if routing_agent_dir.exists():
                # Add the routing agent directory to the path
                sys.path.insert(0, str(routing_agent_dir))
                
                try:
                    # Try the correct import path
                    from routing_agent.agent import routing_agent, AGENTS_AVAILABLE
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
            # Try to use the actual routing agent first
            if self.routing_agent:
                logger.info(f"Processing message with routing agent: {message[:50]}...")
                
                # Create context for the routing agent
                context = {
                    "user_query": message,
                    "user_id": user_id or "anonymous",
                    "session_id": session_id or "default"
                }
                
                # Use the actual routing agent
                try:
                    # Try different approaches to use the routing agent
                    agent_response = None
                    
                    # Approach 1: Try using run_async with proper error handling
                    try:
                        logger.debug("Trying run_async approach...")
                        response = await get_first_asyncgen_result(self.routing_agent.run_async(message))
                        if hasattr(response, 'output') and response.output:
                            agent_response = response.output
                        elif hasattr(response, 'content') and response.content:
                            agent_response = response.content
                        else:
                            agent_response = str(response)
                        logger.debug(f"run_async response: {agent_response}")
                    except Exception as e1:
                        logger.debug(f"run_async failed: {e1}")
                        
                        # Approach 2: Try using run_live with proper error handling
                        try:
                            logger.debug("Trying run_live approach...")
                            response_gen = self.routing_agent.run_live(message)
                            async for response in response_gen:
                                if hasattr(response, 'output') and response.output:
                                    agent_response = response.output
                                elif hasattr(response, 'content') and response.content:
                                    agent_response = response.content
                                else:
                                    agent_response = str(response)
                                break
                            logger.debug(f"run_live response: {agent_response}")
                        except Exception as e2:
                            logger.debug(f"run_live failed: {e2}")
                            
                            # Approach 3: Try using construct method
                            try:
                                logger.debug("Trying construct approach...")
                                # The construct method might need a proper input format
                                response = self.routing_agent.construct({"query": message})
                                if hasattr(response, 'output') and response.output:
                                    agent_response = response.output
                                elif hasattr(response, 'content') and response.content:
                                    agent_response = response.content
                                else:
                                    agent_response = str(response)
                                logger.debug(f"construct response: {agent_response}")
                            except Exception as e3:
                                logger.debug(f"construct failed: {e3}")
                                raise Exception(f"All routing agent approaches failed: {e1}, {e2}, {e3}")
                    
                    # If we got a response, use it
                    if agent_response and not agent_response.startswith("description="):
                        # Determine which agent was used based on the response
                        agent_used = "routing_agent"
                        routing_reason = "Message routed through specialized agent"
                        
                        # Try to extract agent information from the response
                        if "academic" in agent_response.lower():
                            agent_used = "academic_coordinator"
                            routing_reason = "Academic research query detected"
                        elif "fomc" in agent_response.lower() or "federal" in agent_response.lower():
                            agent_used = "fomc_research_agent"
                            routing_reason = "Financial/FOMC query detected"
                        elif "political" in agent_response.lower() or "news" in agent_response.lower():
                            agent_used = "political_news_coordinator"
                            routing_reason = "Political news query detected"
                        
                        return {
                            "success": True,
                            "message": "Message processed successfully by routing agent",
                            "response": agent_response,
                            "agent_used": agent_used,
                            "routing_reason": routing_reason
                        }
                    else:
                        # If routing agent didn't give a proper response, use intelligent simulation
                        logger.info("Routing agent didn't provide proper response, using intelligent simulation")
                        return await self._simulate_routing(message, context)
                    
                except Exception as routing_error:
                    logger.error(f"Routing agent error: {routing_error}")
                    # Fall back to simulation if routing agent fails
                    logger.info("Falling back to simulation mode due to routing agent error")
                    return await self._simulate_routing(message, context)
            
            # If routing agent is not available, use simulation
            logger.info("Using simulation mode - routing agent not available")
            context = {
                "user_query": message,
                "user_id": user_id or "anonymous",
                "session_id": session_id or "default"
            }
            return await self._simulate_routing(message, context)
            
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
        Simulate the routing process when the actual routing agent is not available.
        
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
                "success": True,
                "message": "Message processed successfully (simulation mode)",
                "response": "I'll route this to our Academic Research Agent. This agent specializes in analyzing research papers, finding related literature, and providing research direction suggestions.",
                "agent_used": "academic_coordinator",
                "routing_reason": "Academic research keywords detected (simulation)"
            }
        elif any(keyword in message_lower for keyword in ["fed", "fomc", "federal reserve", "interest rates", "monetary policy", "financial", "market"]):
            return {
                "success": True,
                "message": "Message processed successfully (simulation mode)",
                "response": "I'll route this to our FOMC Research Agent. This agent specializes in analyzing Federal Reserve meetings, financial market implications, and economic policy analysis.",
                "agent_used": "fomc_research_agent",
                "routing_reason": "Financial/FOMC keywords detected (simulation)"
            }
        elif any(keyword in message_lower for keyword in ["political", "news", "government", "election", "policy", "current events"]):
            return {
                "success": True,
                "message": "Message processed successfully (simulation mode)",
                "response": "I'll route this to our Political News Agent. This agent specializes in gathering and analyzing political news from multiple sources with bias detection.",
                "agent_used": "political_news_coordinator",
                "routing_reason": "Political news keywords detected (simulation)"
            }
        else:
            return {
                "success": True,
                "message": "Message processed successfully (simulation mode)",
                "response": "I can help you with academic research, financial analysis, or political news. Please ask me about any of these topics, and I'll route your query to the appropriate specialized agent.",
                "agent_used": "routing_agent",
                "routing_reason": "General inquiry - providing guidance (simulation)"
            }
    
    def get_available_agents(self) -> list:
        """Get list of available specialized agents."""
        return self.available_agents.copy()
    
    def is_available(self) -> bool:
        """Check if the chat service is available."""
        return True  # Always available in simulation mode

# Create a global instance
chat_manager = ChatManager() 