import os
import sys
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ChatManager:
    """Manages chat interactions with the ADK routing agent."""
    
    def __init__(self):
        self.routing_agent_path = None
        self.routing_agent = None
        self._initialize_routing_agent()
    
    def _initialize_routing_agent(self):
        """Initialize the routing agent from its proper directory."""
        try:
            # Find the routing agent directory
            current_dir = Path(__file__).parent.parent
            agents_dir = current_dir / "agents"
            routing_agent_dir = agents_dir / "routing_agent"
            
            if routing_agent_dir.exists():
                self.routing_agent_path = routing_agent_dir
                
                # Add routing agent directory to Python path
                sys.path.insert(0, str(routing_agent_dir))
                
                # Import the routing agent
                from routing_agent.agent import routing_agent
                self.routing_agent = routing_agent
                
                logger.info(f"✅ Routing agent loaded from: {self.routing_agent_path}")
                logger.info(f"✅ Available tools: {[tool.name if hasattr(tool, 'name') else 'Unknown' for tool in self.routing_agent.tools]}")
            else:
                logger.warning("⚠️ Routing agent directory not found, using simulation mode")
                
        except Exception as e:
            logger.error(f"❌ Error loading routing agent: {e}")
            logger.info("🔄 Falling back to simulation mode")
    
    async def process_chat_message(self, message: str, user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Process a chat message using the ADK routing agent.
        
        Args:
            message: The user's message
            user_id: Optional user ID for session management
            session_id: Optional session ID for session management
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            if self.routing_agent is None:
                # Fallback to simulation mode
                return await self._simulate_routing(message, user_id)
            
            # Use the ADK routing agent directly
            try:
                logger.debug("🚀 Using ADK routing agent...")
                
                # Import ADK components
                from google.adk.runners import InMemoryRunner
                from google.genai import types
                
                # Create a runner for the routing agent
                runner = InMemoryRunner(agent=self.routing_agent, app_name="routing_agent")
                
                # Create or use existing session
                if session_id:
                    try:
                        session = await runner.session_service.get_session(
                            app_name=runner.app_name, 
                            user_id=user_id or "default_user",
                            session_id=session_id
                        )
                    except:
                        session = await runner.session_service.create_session(
                            app_name=runner.app_name, 
                            user_id=user_id or "default_user"
                        )
                else:
                    session = await runner.session_service.create_session(
                        app_name=runner.app_name, 
                        user_id=user_id or "default_user"
                    )
                
                # Create content for the message
                content = types.Content(parts=[types.Part(text=message)])
                
                # Run the agent and collect response
                response_content = ""
                agent_used = "routing_agent"
                routing_reason = "Dynamic routing via ADK"
                tool_calls_made = []
                
                async for event in runner.run_async(
                    user_id=session.user_id,
                    session_id=session.id,
                    new_message=content,
                ):
                    logger.debug(f"📡 ADK Event: {type(event)}")
                    
                    # Extract response from event
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts') and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    response_content += part.text
                        elif hasattr(event.content, 'text'):
                            response_content += event.content.text
                    
                    # Check if this is a tool call event (agent routing decision)
                    if hasattr(event, 'tool_calls') and event.tool_calls:
                        for tool_call in event.tool_calls:
                            if hasattr(tool_call, 'name'):
                                tool_calls_made.append(tool_call.name)
                                agent_used = tool_call.name
                                routing_reason = f"Routed to {agent_used} via ADK tool call"
                                logger.info(f"🎯 ADK routed to: {agent_used}")
                    
                    # Check for tool results
                    if hasattr(event, 'tool_results') and event.tool_results:
                        for tool_result in event.tool_results:
                            if hasattr(tool_result, 'content') and tool_result.content:
                                if hasattr(tool_result.content, 'parts') and tool_result.content.parts:
                                    for part in tool_result.content.parts:
                                        if hasattr(part, 'text') and part.text:
                                            response_content += part.text
                                elif hasattr(tool_result.content, 'text'):
                                    response_content += tool_result.content.text
                
                # Clean up session
                await runner.session_service.delete_session(
                    app_name=runner.app_name,
                    user_id=session.user_id,
                    session_id=session.id
                )
                
                if response_content:
                    return {
                        "success": True,
                        "message": "Message processed successfully via ADK routing",
                        "response": response_content,
                        "agent_used": agent_used,
                        "routing_reason": routing_reason,
                        "tool_calls": tool_calls_made,
                        "session_id": session.id,
                        "timestamp": self._get_timestamp()
                    }
                else:
                    logger.warning("⚠️ No response content from ADK routing agent, falling back to simulation")
                    return await self._simulate_routing(message, user_id)
                    
            except Exception as e:
                logger.error(f"❌ Error using ADK routing agent: {e}")
                logger.info("🔄 Falling back to simulation mode")
                return await self._simulate_routing(message, user_id)
                
        except Exception as e:
            logger.error(f"❌ Error in process_chat_message: {e}")
            return {
                "success": False,
                "message": f"Error processing message: {str(e)}",
                "response": "I apologize, but I encountered an error processing your request.",
                "agent_used": "error",
                "routing_reason": "Error occurred",
                "timestamp": self._get_timestamp()
            }
    
    async def _simulate_routing(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """Simulate routing logic when the actual routing agent is not available."""
        message_lower = message.lower()
        
        # Simple keyword-based routing
        if any(keyword in message_lower for keyword in ["research", "paper", "academic", "study", "analysis", "literature"]):
            agent_used = "academic_coordinator"
            routing_reason = "Academic research keywords detected (simulation)"
            response = "I'll route this to our Academic Research Agent. This agent specializes in research analysis, literature reviews, and academic guidance."
            
        elif any(keyword in message_lower for keyword in ["fed", "fomc", "federal reserve", "interest rate", "monetary policy", "economic policy"]):
            agent_used = "fomc_research_agent"
            routing_reason = "FOMC/economic policy keywords detected (simulation)"
            response = "I'll route this to our FOMC Research Agent. This agent specializes in Federal Reserve analysis, monetary policy research, and economic insights."
            
        elif any(keyword in message_lower for keyword in ["news", "political", "politics", "election", "government", "policy", "current events"]):
            agent_used = "political_news_coordinator"
            routing_reason = "Political news keywords detected (simulation)"
            response = "I'll route this to our Political News Agent. This agent specializes in gathering and analyzing political news from multiple sources with bias detection."
            
        else:
            agent_used = "general_assistant"
            routing_reason = "General query (simulation)"
            response = "I'm here to help! I can assist with academic research, FOMC analysis, political news, or general questions. What would you like to know?"
        
        return {
            "success": True,
            "message": "Message processed successfully (simulation mode)",
            "response": response,
            "agent_used": agent_used,
            "routing_reason": routing_reason,
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()

# Create a global instance
chat_manager = ChatManager() 