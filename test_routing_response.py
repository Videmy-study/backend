import sys
import asyncio
from pathlib import Path
import logging

# Add the routing agent to the path
current_dir = Path(__file__).parent
agents_dir = current_dir / "agents"
routing_agent_dir = agents_dir / "routing_agent"
sys.path.insert(0, str(routing_agent_dir))

from routing_agent.agent import routing_agent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_routing_response():
    try:
        print("Testing routing agent response with construct method...")
        
        # Try using the construct method instead
        response = routing_agent.construct("Can you help me with academic research?")
        logger.debug(f"Construct response type: {type(response)}; Value: {response}")
        
        if hasattr(response, 'output'):
            print(f"Output: {response.output}")
        if hasattr(response, 'content'):
            print(f"Content: {response.content}")
        if hasattr(response, 'text'):
            print(f"Text: {response.text}")
        if hasattr(response, 'message'):
            print(f"Message: {response.message}")
            
    except Exception as e:
        logger.error(f"Error with construct: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Try run_live as fallback
        try:
            print("\nTrying run_live as fallback...")
            response_gen = routing_agent.run_live("Can you help me with academic research?")
            async for response in response_gen:
                logger.debug(f"Yielded type: {type(response)}; Value: {response}")
                if hasattr(response, 'output'):
                    print(f"Output: {response.output}")
                if hasattr(response, 'content'):
                    print(f"Content: {response.content}")
                if hasattr(response, 'text'):
                    print(f"Text: {response.text}")
                if hasattr(response, 'message'):
                    print(f"Message: {response.message}")
                break
        except Exception as e2:
            logger.error(f"Error with run_live fallback: {e2}")
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test_routing_response()) 