#!/usr/bin/env python3
"""Script to create .env file for Vertex AI with Gemini API key."""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with the correct environment variables."""
    
    env_content = """# Environment variables for Vertex AI with Gemini API key
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_API_KEY=your-gemini-api-key-here
GOOGLE_PLACES_API_KEY=your-places-api-key-here

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
    else:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"✅ Created .env file at {env_file}")
        print("   Please update it with your actual API keys:")
        print("   - Replace 'your-gemini-api-key-here' with your actual Gemini API key")
        print("   - Replace 'your-places-api-key-here' with your actual Places API key (if needed)")
    
    print("\n📋 Instructions:")
    print("1. Edit the .env file and replace the placeholder values with your actual API keys")
    print("2. Make sure GOOGLE_GENAI_USE_VERTEXAI=true is set")
    print("3. Run: python test_simple_imports.py to test the setup")

if __name__ == "__main__":
    create_env_file() 