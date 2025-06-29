import pathlib
from beanie import Document, Link, Indexed
from pydantic import Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum

class VideoStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"

# Video model
class Video(Document):
    generation_prompt: str = Field(..., min_length=1, max_length=1000, description="Prompt used to generate the video")
    scheduled_time: Optional[datetime] = Field(None, description="Scheduled time for posting the video")
    video_url: str = Field(..., min_length=1, description="URL of the video")
    hashtags: List[str] = Field(default=[], description="List of hashtags for the video")
    caption: Optional[str] = Field(None, max_length=2200, description="Caption for the video")
    status: Optional[VideoStatus] = Field(None, description="Status of the video (e.g., 'draft', 'scheduled', 'posted')")
    insta_acc_id: Link["InstagramAccount"] = Field(..., description="Reference to the Instagram account")
    user_id: Link["User"] = Field(..., description="Reference to the user")

    class Settings:
        name = "videos"
        indexes = [
            [("generation_prompt", 1)],  # Index for searching by prompt
            [("scheduled_time", -1)],   # Index for sorting by scheduled time
            [("status", 1)],            # Index for filtering by status
        ]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            ObjectId: str,
        }

# InstagramAcc model
class InstagramAccount(Document):
    username: str = Field(Indexed(unique=True), min_length=1, max_length=30, description="Instagram username")
    password: str = Field(..., min_length=8, description="Hashed password for the Instagram account")
    instagram_user_id: str = Field(..., description="Instagram's unique user ID")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name of the account owner")
    bio: Optional[str] = Field(None, max_length=150, description="Instagram bio")
    follower_count: int = Field(..., ge=0, description="Number of followers")
    following_count: int = Field(..., ge=0, description="Number of accounts followed")
    session_data: Optional[str] = Field(None, description="Serialized session data for the Instagram account")
    media_count: int = Field(..., ge=0, description="Number of posts")
    video_ids: List[Link[Video]] = Field(default=[], description="List of video references")

    class Settings:
        name = "instagram_accounts"
        indexes = [
            [("instagram_user_id", 1), ("username", 1)],  # Composite index for unique Instagram user ID and username
        ]

    class Config:
        json_encoders = {
            ObjectId: str,
        }

# User model
class User(Document):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(Indexed(unique=True), description="User's email address")
    password: str = Field(..., min_length=8, description="Hashed password")
    insta_acc_ids: List[Link[InstagramAccount]] = Field(default=[], description="List of Instagram account references")
    videos_ids: List[Link[Video]] = Field(default=[], description="List of video references")

    class Settings:
        name = "users"
        indexes = [
            [("email", 1)],  # Index for email-based lookups
        ]

    class Config:
        json_encoders = {
            ObjectId: str,
        }

# Get the directory of the current file (i.e., backend/database)
_current_dir = pathlib.Path(__file__).parent
# Get the backend directory, then create a 'storage' directory inside it
_storage_dir = _current_dir.parent / "storage"
_storage_dir.mkdir(exist_ok=True)