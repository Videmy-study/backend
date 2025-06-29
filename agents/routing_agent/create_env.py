#!/usr/bin/env python3
"""Script to create .env file for Vertex AI with Gemini API key and Political News API keys."""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with the correct environment variables."""
    
    env_content = """# Environment variables for Vertex AI with Gemini API key
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_API_KEY=your-gemini-api-key-here
GOOGLE_PLACES_API_KEY=your-places-api-key-here

# Political News API Keys (required for political news agent)
NEWSAPI_KEY=your-newsapi-key-here
GNEWS_API_KEY=your-gnews-api-key-here
MEDIASTACK_API_KEY=your-mediastack-api-key-here
NEWSDATA_API_KEY=your-newsdata-api-key-here

# Optional: Google Cloud project settings (if using Vertex AI)
# GOOGLE_CLOUD_PROJECT=your-gcp-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
"""
    
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print(f"⚠️  .env file already exists at {env_file}")
        print("   Please update it manually with your API keys:")
        print("   - Replace 'your-gemini-api-key-here' with your actual Gemini API key")
        print("   - Replace 'your-places-api-key-here' with your actual Places API key (if needed)")
        print("   - Replace political news API keys with your actual keys:")
        print("     * NEWSAPI_KEY: Get from https://newsapi.org/")
        print("     * GNEWS_API_KEY: Get from https://gnews.io/")
        print("     * MEDIASTACK_API_KEY: Get from https://mediastack.com/")
        print("     * NEWSDATA_API_KEY: Get from https://newsdata.io/")
    else:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"✅ Created .env file at {env_file}")
        print("   Please update it with your actual API keys:")
        print("   - Replace 'your-gemini-api-key-here' with your actual Gemini API key")
        print("   - Replace 'your-places-api-key-here' with your actual Places API key (if needed)")
        print("   - Replace political news API keys with your actual keys:")
        print("     * NEWSAPI_KEY: Get from https://newsapi.org/")
        print("     * GNEWS_API_KEY: Get from https://gnews.io/")
        print("     * MEDIASTACK_API_KEY: Get from https://mediastack.com/")
        print("     * NEWSDATA_API_KEY: Get from https://newsdata.io/")
    
    print("\n📋 Instructions:")
    print("1. Edit the .env file and replace the placeholder values with your actual API keys")
    print("2. Make sure GOOGLE_GENAI_USE_VERTEXAI=true is set")
    print("3. At least one political news API key is required for the political news agent to work")
    print("4. Run: python test_simple_imports.py to test the setup")

if __name__ == "__main__":
    create_env_file() 