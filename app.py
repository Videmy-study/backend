import os
from dotenv import load_dotenv
from fastapi import FastAPI
from beanie import init_beanie
from database.schemas import Video, InstagramAccount, User
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

load_dotenv()

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB connection and Beanie
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    await init_beanie(database=client["gdg-solutionhacks"], document_models=[Video, InstagramAccount, User])

    ####### temp
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
    title="GDG Solution Hacks API",
    description="A basic FastAPI server for the hackathon project",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)