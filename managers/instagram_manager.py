import json
from typing import Dict, Optional, List
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes, RateLimitError
from database.schemas import InstagramAccount

class InstagramManager:
    def __init__(self):
        self.clients: Dict[str, Client] = {}
    
    async def add_account(self, username: str, password: str) -> tuple[bool, str]:
        try:
            existing = await InstagramAccount.find_one(InstagramAccount.username == username)
            if existing:
                return False, "Account already exists"
            
            client = Client()
            
            try:
                client.login(username, password)
            except ChallengeRequired as e:
                return False, "Instagram challenge required - please complete verification"
            except LoginRequired as e:
                return False, "Invalid credentials or login blocked"
            except PleaseWaitFewMinutes as e:
                return False, "Rate limited - please wait a few minutes"
            except RateLimitError as e:
                return False, "Too many requests - please try again later"
            except Exception as e:
                return False, f"Login failed: {str(e)}"
            
            try:
                user_info = client.user_info(str(client.user_id))
                full_name = getattr(user_info, 'full_name', username)
                bio = getattr(user_info, 'biography', '')
                follower_count = getattr(user_info, 'follower_count', 0)
                following_count = getattr(user_info, 'following_count', 0)
                media_count = getattr(user_info, 'media_count', 0)
            except Exception as e:
                full_name = username
                bio = ''
                follower_count = 0
                following_count = 0
                media_count = 0
            
            account = InstagramAccount(
                username=username,
                password=password,
                instagram_user_id=str(client.user_id),
                full_name=full_name,
                bio=bio,
                follower_count=follower_count,
                following_count=following_count,
                media_count=media_count,
                session_data=json.dumps(client.get_settings())
            )
            
            await account.save()
            
            self.clients[username] = client
            return True, "Account added successfully"
            
        except Exception as e:
            return False, f"Database error: {str(e)}"
    
    async def load_account(self, username: str) -> tuple[bool, str]:
        try:
            account = await InstagramAccount.find_one(InstagramAccount.username == username)
            if not account:
                return False, "Account not found"
            
            try:
                client = Client()
                session_data = account.session_data
                if session_data is None:
                    return False, "No session data found"
                settings = json.loads(session_data)
                client.set_settings(settings)
                
                try:
                    client.account_info()
                    self.clients[username] = client
                    return True, "Session loaded successfully"
                except LoginRequired:
                    return False, "Session expired - please re-login"
                    
            except json.JSONDecodeError as e:
                return False, "Invalid session data"
            except Exception as e:
                return False, f"Session restore failed: {str(e)}"
                
        except Exception as e:
            return False, f"Database error: {str(e)}"
        
    async def upload_video(self, username: str, video_path: str, caption: str = "") -> tuple[Optional[str], str]:
        if username not in self.clients:
            success, message = await self.load_account(username)
            if not success:
                return None, message
        
        try:
            client = self.clients[username]
            media = client.clip_upload(Path(video_path), caption)
            return str(media.id), "Video uploaded successfully"
        except LoginRequired as e:
            return None, "Session expired - please re-login"
        except RateLimitError as e:
            return None, "Rate limited - please try again later"
        except Exception as e:
            return None, f"Upload failed: {str(e)}"

    
    async def update_account_stats(self, username: str) -> bool:
        if username not in self.clients:
            if not self.load_account(username):
                return False
        
        try:
            client = self.clients[username]
            user_info = client.user_info(str(client.user_id))
            
            account = await InstagramAccount.find_one(InstagramAccount.username == username)
            if account:
                account.follower_count = user_info.follower_count
                account.following_count = user_info.following_count
                account.media_count = user_info.media_count
                account.session_data = json.dumps(client.get_settings())
                await account.save()
                return True
        except Exception as e:
            print(f"Failed to update stats for {username}: {e}")
        
        return False
    
    async def get_account_info(self, username: str) -> Optional[dict]:
        try:
            account = await InstagramAccount.find_one(InstagramAccount.username == username)
            if account:
                return {
                    'username': account.username,
                    'full_name': account.full_name,
                    'bio': account.bio,
                    'follower_count': account.follower_count,
                    'following_count': account.following_count,
                    'media_count': account.media_count,
                }
            
        except Exception as e:
            print(f"Failed to get info for {username}: {e}")
        
        return None
    
    async def list_accounts(self) -> List[str]:
        try:
            accounts = await InstagramAccount.find().to_list()
            return [account.username for account in accounts]
        except Exception as e:
            print(f"Failed to list accounts: {e}")
            return []
    
    async def remove_account(self, username: str) -> bool:
        try:
            account = await InstagramAccount.find_one(InstagramAccount.username == username)
            if account:
                await account.delete()
                
                if username in self.clients:
                    del self.clients[username]
                
                return True
        except Exception as e:
            print(f"Failed to remove account {username}: {e}")
        
        return False