from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from database.schemas import VideoStatus
from datetime import datetime
from enum import Enum

# Response schemas for API responses
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None

# Video schemas
class VideoBase(BaseModel):
    generation_prompt: str = Field(..., min_length=1, max_length=1000)
    scheduled_time: Optional[datetime] = None
    video_url: str
    hashtags: List[str] = []
    caption: Optional[str] = None
    status: Optional[VideoStatus] = None

class VideoCreate(BaseModel):
    generation_prompt: str = Field(..., min_length=1, max_length=1000)
    user_id: str
    insta_acc_id: str

class VideoUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    status: Optional[VideoStatus] = None

class VideoOut(VideoBase):
    id: str
    insta_acc_id: str
    user_id: str
    created_at: Optional[datetime] = None


    class Config:
        from_attributes = True

# Instagram Account schemas
class InstagramAccountBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=150)

class InstagramAccountCreate(InstagramAccountBase):
    password: str = Field(..., min_length=8)

class InstagramAccountLogin(BaseModel):
    username: str
    password: str

class InstagramAccountUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None

class InstagramAccountOut(InstagramAccountBase):
    id: str
    instagram_user_id: str
    follower_count: int
    following_count: int
    media_count: int
    session_data: Optional[str] = None

    class Config:
        from_attributes = True

class InstagramAccountInfo(BaseModel):
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    follower_count: int
    following_count: int
    media_count: int

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(UserBase):
    id: str
    insta_acc_ids: List[str] = []
    videos_ids: List[str] = []

    class Config:
        from_attributes = True

# Video Generation schemas
class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    user_id: str
    insta_acc_id: str

class VideoGenerationResponse(BaseModel):
    success: bool
    video_id: Optional[str] = None
    message: str
    video_url: Optional[str] = None

# Instagram Upload schemas
class VideoUploadRequest(BaseModel):
    id: str
    username: str
    video_path: str
    caption: Optional[str] = ""

class VideoUploadResponse(BaseModel):
    success: bool
    media_id: Optional[str] = None
    message: str

# Account Management schemas
class AccountListResponse(BaseModel):
    accounts: List[str]

class AccountStatsUpdate(BaseModel):
    username: str

class AccountStatsResponse(BaseModel):
    success: bool
    message: str
    stats: Optional[Dict[str, int]] = None

# Caption and Tags schemas
class CaptionTagsRequest(BaseModel):
    original_prompt: str = Field(..., min_length=1, max_length=1000)

class CaptionTagsResponse(BaseModel):
    caption: str
    hashtags: List[str]
    prompt: str