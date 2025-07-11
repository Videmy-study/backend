import os
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from beanie import init_beanie, PydanticObjectId
from database.schemas import Video, InstagramAccount, User, VideoStatus
from managers.instagram_manager import InstagramManager
from managers.vid_generator import generate, give_captions_and_tags
from managers.chat_manager_clean import chat_manager
from api.schemas import (
    InstagramAccountCreate, InstagramAccountOut, AccountListResponse,
    VideoOut, VideoUpdate, VideoGenerationRequest, 
    VideoGenerationResponse, VideoUploadRequest, VideoUploadResponse,
    CaptionTagsRequest, CaptionTagsResponse, 
    AccountStatsResponse, SuccessResponse, ChatRequest, ChatResponse,
)
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pathlib import Path
from datetime import datetime
import logging

load_dotenv()

scheduler = AsyncIOScheduler()
instagram_manager = InstagramManager()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB connection and Beanie
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    await init_beanie(database=client["gdg-solutionhacks"], document_models=[Video, InstagramAccount, User])

    def something_to_run_every_24_hours():
        print("Running scheduled task to update videos...")

    scheduler.start()
    scheduler.add_job(
        something_to_run_every_24_hours,
        trigger=IntervalTrigger(hours=24),
        id="update_scheduled_videos",
        replace_existing=True
    )
    
    yield
    # Shutdown: Close scheduler and MongoDB connection
    scheduler.shutdown()
    client.close()

# Create FastAPI instance
app = FastAPI(
    title="Videmy Study API",
    description="API for AI-powered research platform with specialized agents",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:4173",
        "https://getreals.club",
        "https://getrealsclub.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that routes messages to appropriate specialized agents.
    """
    try:
        # Process the message using the chat manager
        result = await chat_manager.process_chat_message(
            message=request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        # Return the response
        return ChatResponse(
            success=result["success"],
            message=result["message"],
            response=result["response"],
            agent_used=result["agent_used"],
            routing_reason=result["routing_reason"],
            timestamp=result["timestamp"],
            session_id=result.get("session_id"),
            tool_calls=result.get("tool_calls", [])
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            success=False,
            message=f"Error processing chat request: {str(e)}",
            response="I apologize, but I encountered an error processing your request.",
            agent_used="error",
            routing_reason="Error occurred",
            timestamp=datetime.now().isoformat()
        )

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

@app.post("/instagram-accounts/", response_model=InstagramAccountOut)
async def create_instagram_account(account: InstagramAccountCreate):
    """Add a new Instagram account"""
    try:
        success, message = await instagram_manager.add_account(account.username, account.password)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        # Get the created account
        instagram_account = await InstagramAccount.find_one(InstagramAccount.username == account.username)
        if not instagram_account:
            raise HTTPException(status_code=500, detail="Failed to retrieve created account")
        
        return InstagramAccountOut(
            id=str(instagram_account.id),
            username=instagram_account.username,
            full_name=instagram_account.full_name,
            bio=instagram_account.bio,
            instagram_user_id=instagram_account.instagram_user_id,
            follower_count=instagram_account.follower_count,
            following_count=instagram_account.following_count,
            media_count=instagram_account.media_count,
            session_data=instagram_account.session_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Instagram account: {str(e)}")

@app.get("/instagram-accounts/{account_id}", response_model=InstagramAccountOut)
async def get_instagram_account(account_id: str):
    """Get Instagram account by ID"""
    try:
        account = await InstagramAccount.get(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Instagram account not found")
        
        return InstagramAccountOut(
            id=str(account.id),
            username=account.username,
            full_name=account.full_name,
            bio=account.bio,
            instagram_user_id=account.instagram_user_id,
            follower_count=account.follower_count,
            following_count=account.following_count,
            media_count=account.media_count,
            session_data=account.session_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Instagram account: {str(e)}")

@app.get("/instagram-accounts/", response_model=AccountListResponse)
async def list_instagram_accounts():
    """List all Instagram accounts"""
    try:
        accounts = await instagram_manager.list_accounts()
        return AccountListResponse(accounts=accounts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list accounts: {str(e)}")

@app.post("/instagram-accounts/{username}/load", response_model=SuccessResponse)
async def load_instagram_account(username: str):
    """Load Instagram account session"""
    try:
        success, message = await instagram_manager.load_account(username)
        return SuccessResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load account: {str(e)}")

@app.post("/instagram-accounts/{username}/update-stats", response_model=AccountStatsResponse)
async def update_account_stats(username: str):
    """Update Instagram account statistics"""
    try:
        success = await instagram_manager.update_account_stats(username)
        if success:
            account_info = await instagram_manager.get_account_info(username)
            return AccountStatsResponse(
                success=True,
                message="Account stats updated successfully",
                stats=account_info
            )
        else:
            return AccountStatsResponse(success=False, message="Failed to update account stats")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update account stats: {str(e)}")

@app.delete("/instagram-accounts/{username}", response_model=SuccessResponse)
async def remove_instagram_account(username: str):
    """Remove Instagram account"""
    try:
        success = await instagram_manager.remove_account(username)
        if success:
            return SuccessResponse(success=True, message="Account removed successfully")
        else:
            return SuccessResponse(success=False, message="Failed to remove account")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove account: {str(e)}")

@app.post("/videos/generate/", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """Generate a new video using AI"""
    try:
        video = await generate(request.prompt, request.user_id, request.insta_acc_id)
        if video:
            return VideoGenerationResponse(
                success=True,
                video_id=str(video.id),
                message="Video generated successfully",
                video_url=video.video_url
            )
        else:
            return VideoGenerationResponse(
                success=False,
                message="Failed to generate video"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")

@app.post("/videos/captions-tags/", response_model=CaptionTagsResponse)
async def generate_captions_and_tags(request: CaptionTagsRequest):
    """Generate captions and hashtags for a video prompt"""
    try:
        result = await give_captions_and_tags(request.original_prompt)
        if result:
            return CaptionTagsResponse(
                caption=result.get("caption", ""),
                hashtags=result.get("hashtags", []),
                prompt=result.get("prompt", "")
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate captions and tags")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate captions and tags: {str(e)}")

@app.get("/videos/", response_model=List[VideoOut])
async def list_videos():
    """List all videos"""
    try:
        videos = await Video.find_all().to_list()
        result = []
        for video in videos:
            # Fetch linked documents
            insta_acc = await video.insta_acc_id.fetch()
            user = await video.user_id.fetch()
            
            result.append(VideoOut(
                id=str(video.id),
                generation_prompt=video.generation_prompt,
                scheduled_time=video.scheduled_time,
                video_url=video.video_url,
                hashtags=video.hashtags,
                caption=video.caption,
                status=video.status,
                insta_acc_id=str(insta_acc) if insta_acc else "",
                user_id=str(user) if user else ""
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list videos: {str(e)}")

@app.get("/videos/{video_id}", response_model=VideoOut)
async def get_video(video_id: str):
    """Get video by ID"""
    try:
        video = await Video.get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Fetch linked documents
        insta_acc = await video.insta_acc_id.fetch()
        user = await video.user_id.fetch()
        
        return VideoOut(
            id=str(video.id),
            generation_prompt=video.generation_prompt,
            scheduled_time=video.scheduled_time,
            video_url=video.video_url,
            hashtags=video.hashtags,
            caption=video.caption,
            status=video.status,
            insta_acc_id=str(insta_acc) if insta_acc else "",
            user_id=str(user) if user else ""
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get video: {str(e)}")

@app.put("/videos/{video_id}", response_model=VideoOut)
async def update_video(video_id: str, video_update: VideoUpdate):
    """Update video information"""
    try:
        video = await Video.get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        if video_update.scheduled_time is not None:
            video.scheduled_time = video_update.scheduled_time
        if video_update.caption is not None:
            video.caption = video_update.caption
        if video_update.hashtags is not None:
            video.hashtags = video_update.hashtags
        if video_update.status is not None:
            video.status = video_update.status
        
        await video.save()
        
        # Fetch linked documents
        insta_acc = await video.insta_acc_id.fetch()
        user = await video.user_id.fetch()
        
        return VideoOut(
            id=str(video.id),
            generation_prompt=video.generation_prompt,
            scheduled_time=video.scheduled_time,
            video_url=video.video_url,
            hashtags=video.hashtags,
            caption=video.caption,
            status=video.status,
            insta_acc_id=str(insta_acc) if insta_acc else "",
            user_id=str(user) if user else ""
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update video: {str(e)}")

@app.delete("/videos/{video_id}", response_model=SuccessResponse)
async def delete_video(video_id: str):
    """Delete a video"""
    try:
        video = await Video.get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        await video.delete()
        return SuccessResponse(success=True, message="Video deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete video: {str(e)}")

@app.post("/instagram-upload/", response_model=VideoUploadResponse)
async def upload_video_to_instagram(request: VideoUploadRequest):
    """Upload video to Instagram"""
    try:
        video = await Video.get(request.id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        media_id, message = await instagram_manager.upload_video(
            request.username, 
            video.video_path, 
            video.caption if video.caption else ""
        )
        
        return VideoUploadResponse(
            success=media_id is not None,
            media_id=media_id,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload video: {str(e)}")

@app.get("/videos/{video_id}/download")
async def download_video(video_id: str):
    """Download video file"""
    try:
        video = await Video.get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Check if file exists
        video_path = Path(f"storage/{video.video_path}")
        if not video_path.exists():
            raise HTTPException(status_code=404, detail="Video file not found")
        
        return FileResponse(
            path=video_path,
            filename=video.video_path,
            media_type="video/mp4"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download video: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)