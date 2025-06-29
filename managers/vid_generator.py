import os
import time
import uuid
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from beanie import Link
from database.schemas import Video, VideoStatus, InstagramAccount, User

load_dotenv("../.env")

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
)

text_config = types.GenerateContentConfig(
    response_mime_type="text/plain",
)

import json

async def give_captions_and_tags(original_prompt: str):
    model = "gemini-2.0-flash"
    prompt = f"""
You are an expert social media video creator.

Given the following main video idea prompt:
"{original_prompt}"

Fill in the following fields and return ONLY valid JSON (no extra text):

{{
  "caption": "<A catchy, engaging caption for the video (max 2200 characters)>",
  "hashtags": ["<hashtag1>", "<hashtag2>", "<hashtag3>", "..."],  // 5-10 relevant hashtags,
  "prompt": "<Write a 10-15 second dialogue script on the basis of video idea prompt for a created named "Kate" speaking directly to the camera, packed with brain-rot humor and slang to entertain younger audiences. The dialogue should be a single continuous paragraph with no delimiters, stage directions, or extra descriptions—just the spoken words. Start with the creator hyping up their 'Skibidi toilet' obsession, then flex their 'Rizzler' status with phrases like 'GYATT on 100,' 'Ohio who?', and 'W or L only.' Include chaotic Gen Alpha slang like 'YEET,' 'BRUH,' and 'Rizzler mode' to keep the energy unhinged. End with a bold closer like 'Only Rizzlers survive' to hype the audience. Ensure the dialogue flows naturally, feels absurdly meme-heavy, and fits a 10-15 second delivery for a fast-paced social media video.>(max 100 words)"
}}
"""
    contents = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=prompt),
        ],
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=text_config,
    ):
        response += str(chunk.text)

    # Try to parse the response as JSON
    try:
        start = response.find("{")
        end = response.rfind("}") + 1    
        return json.loads(response[start:end])
    except Exception as e:
        print("Failed to parse AI response as JSON:", e)
        result = None

    return result

async def generate(prompt: str, user_id: str, insta_acc_id: str):
    # Fetch the actual documents to create proper Link objects
    user = await User.get(user_id)
    insta_acc = await InstagramAccount.get(insta_acc_id)

    captions_tags = await give_captions_and_tags(prompt)
    if not captions_tags:
        print("Failed to generate captions, tags, and scenes")
        return

    url = "https://api.captions.ai/api/ads"

    headers = {
        "x-api-key": os.getenv("CAPTIONS_API_KEY"),
        "Content-Type": "application/json"
    }

    payload = {
        "script": captions_tags["prompt"],
        "creatorName": "Kate",
        "mediaUrls": [
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHROih5p2yLYnHROVl5XJ2suCxDjKBP0c4W7TaMN",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHROy3wMC5bX40QiFdVDRrqTNOIUtfx83ApJgcZ5", 
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHROw42Mxc7Pk0vj8WqyAMb2R5hYc3us7H69zdeS",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHROTHLMkODSLz5DayZfGBPqY8CUJgW0EvhHe97b",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHRO2DjsqfT5JyvCIUBlOEhNQMVrdfewzDmxYLTc",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHRO8mJk9pWhJzsZU5XQi7kwILNWu1OAhBd4qnPt",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHROLQt86mYxDnq6Qr3cFHUAG9pJuCXfPokadtZw",
            "https://gw42iab886.ufs.sh/f/ixsAdYLYnHRODz4sApPUgZsPrI9xfW7mFXNeL1aBiz6GuopC"
        ]
    }

    response = requests.request("POST", f"{url}/submit", json=payload, headers=headers)
    
    operationId = response.json().get("operationId")

    payload = {
        "operationId": operationId,
    }

    json_response = None

    try:
        while True:
            response = requests.request("POST", f"{url}/poll", json=payload, headers=headers)
            json_response = response.json()
            if "progress" not in json_response:
                raise Exception("Invalid response format, 'state' key not found")
            time.sleep(60)
    except Exception as e:
        try:
            # Check if json_response is valid and contains the "url" key
            if json_response and "url" in json_response:
                # Send a GET request to the URL
                response = requests.get(json_response["url"], stream=True)
                uuid_str = str(uuid.uuid4())  # Generate a unique identifier for the video file
                # Check if the request was successful
                if response.status_code == 200 and insta_acc and user:
                    # Open a file in binary write mode and save the video
                    with open(f"video_{uuid_str}.mp4", "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    video = Video(
                        generation_prompt=prompt,
                        scheduled_time=None,  # Set to None for now, can be updated later
                        video_url=f"video_{uuid_str}.mp4",
                        hashtags=captions_tags["hashtags"],
                        caption=captions_tags["caption"],
                        status=VideoStatus.DRAFT,
                        insta_acc_id=Link(insta_acc.to_ref(), InstagramAccount),
                        user_id=Link(user.to_ref(), User)
                    )
                    await video.save()
                    print(f"Video downloaded successfully as video.mp4")
                else:
                    print(f"Failed to download video. Status code: {response.status_code}")
            else:
                print("No valid URL found in json_response to download the video.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")