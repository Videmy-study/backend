import requests

async def get_current_events():
    """
    Fetches the current events from the Videmy Study API.
    
    Returns:
        list: A list of current events.
    """
    try:
        response = requests.post("http://localhost:8000/chat", json={})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching current events: {e}")
        return []