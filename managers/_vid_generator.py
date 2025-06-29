# import time
# import os
# import uuid
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from beanie import Link
# # from database.schemas import Video, VideoStatus, InstagramAccount, User

# load_dotenv()

# MODEL = "veo-2.0-generate-001"

# client = genai.Client(
#     http_options={"api_version": "v1beta"},
#     api_key=os.getenv("GOOGLE_API_KEY"),
# )

# video_config = types.GenerateVideosConfig(
#     person_generation="allow_all", # supported values: "dont_allow" or "allow_adult" or "allow_all"
#     aspect_ratio="9:16", # supported values: "16:9" or "16:10"
#     number_of_videos=1, # supported values: 1 - 4
#     duration_seconds=8, # supported values: 5 - 8
# )

# text_config = types.GenerateContentConfig(
#     response_mime_type="text/plain",
# )

# import json

# async def give_captions_tags_and_scenes(original_prompt: str):
#     model = "gemini-2.0-flash"
#     prompt = f"""
# You are an expert social media video creator.

# Given the following main video idea prompt:
# "{original_prompt}"

# Fill in the following fields and return ONLY valid JSON (no extra text):

# {{
#   "caption": "<A catchy, engaging caption for the video (max 2200 characters)>",
#   "hashtags": ["<hashtag1>", "<hashtag2>", "<hashtag3>", "..."],  // 5-10 relevant hashtags
#   "scenes": [
#     "<Description of scene 1 (3-5 seconds)>",
#     "<Description of scene 2 (3-5 seconds)>",
#     "<Description of scene 3 (3-5 seconds)>"
#     // Add more scenes if needed, each 3-5 seconds long
#   ]
# }}
# """
#     contents = types.Content(
#         role="user",
#         parts=[
#             types.Part.from_text(text=prompt),
#         ],
#     )

#     response = ""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=text_config,
#     ):
#         response += str(chunk.text)

#     # Try to parse the response as JSON
#     try:
#         start = response.find("{")
#         end = response.rfind("}") + 1    
#         return json.loads(response[start:end])
#     except Exception as e:
#         print("Failed to parse AI response as JSON:", e)
#         result = None

#     return result

# async def generate(prompt: str, user_id: str, insta_acc_id: str):
#     # Fetch the actual documents to create proper Link objects
#     # user = await User.get(user_id)
#     # insta_acc = await InstagramAccount.get(insta_acc_id)

#     captions_tags_scenes = await give_captions_tags_and_scenes(prompt)
#     if not captions_tags_scenes:
#         print("Failed to generate captions, tags, and scenes")
#         return

#     uuid_str = str(uuid.uuid4())
    
#     for scene in captions_tags_scenes["scenes"]:
#         prompt = f"""
#         generate a video with the following scene:
#         {scene}
#         """

#         operation = client.models.generate_videos(
#             model=MODEL,
#             prompt=prompt,
#             config=video_config,
#         )

#         # Waiting for the video(s) to be generated
#         while not operation.done:
#             print("Video has not been generated yet. Check again in 10 seconds...")
#             time.sleep(10)
#             operation = client.operations.get(operation)

#         result = operation.result
#         if not result:
#             print("Error occurred while generating video.")
#             return

#         generated_videos = result.generated_videos
#         if not generated_videos:
#             print("No videos were generated.")
#             return

#         print(f"Generated {len(generated_videos)} video(s).")
#         for n, generated_video in enumerate(generated_videos):
#             if generated_video.video is not None:
#                 print(f"Video has been generated: {generated_video.video.uri}")
#                 client.files.download(file=generated_video.video)
#                 generated_video.video.save(f"video_{uuid_str}_{n}.mp4") # Saves the video(s)

#                 # video = Video(
#                 #     generation_prompt=prompt,
#                 #     scheduled_time=None,  # Set appropriate datetime if available
#                 #     video_url=f"video_{uuid_str}_{n}.mp4",
#                 #     caption="",  # Set appropriate caption if available
#                 #     status=VideoStatus.DRAFT,  # Set appropriate status if available
#                 #     insta_acc_id=Link(insta_acc.to_ref(), InstagramAccount),
#                 #     user_id=Link(user.to_ref(), User),
#                 # )
#                 # await video.save()

#                 print(f"Video {generated_video.video.uri} has been downloaded to video_{uuid_str}_{n}.mp4.")
#             else:
#                 print("No video file found for this generated video.")

# if __name__ == "__main__":
#     import asyncio

#     # Example usage
#     prompt = "Create a video about the importance of mental health awareness."
#     user_id = "60c72b2f9b1e8b001c8e4d3a"  # Replace with actual user ID
#     insta_acc_id = "60c72b2f9b1e8b001c8e4d3b"  # Replace with actual Instagram account ID

#     asyncio.run(generate(prompt, user_id, insta_acc_id))