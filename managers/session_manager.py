import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Represents a single chat message in a conversation."""
    message_id: str
    user_id: str
    session_id: str
    message: str
    response: str
    agent_used: Optional[str]
    routing_reason: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class ChatSession:
    """Represents a chat session with conversation history."""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    message_count: int
    is_active: bool
    metadata: Dict[str, Any]

class SessionManager:
    """Manages chat sessions and conversation history."""
    
    def __init__(self, session_timeout_hours: int = 24):
        self.sessions: Dict[str, ChatSession] = {}
        self.conversations: Dict[str, List[ChatMessage]] = {}
        self.session_timeout_hours = session_timeout_hours
        self._cleanup_interval = 3600  # Clean up every hour
        self._last_cleanup = time.time()
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session_{uuid.uuid4().hex[:16]}"
    
    def generate_user_id(self) -> str:
        """Generate a unique user ID for anonymous users."""
        return f"user_{uuid.uuid4().hex[:12]}"
    
    def create_session(self, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new chat session.
        
        Args:
            user_id: Optional user ID. If None, generates an anonymous user ID
            metadata: Optional metadata for the session
            
        Returns:
            Session ID
        """
        # Generate user ID if not provided
        if not user_id:
            user_id = self.generate_user_id()
        
        # Generate session ID
        session_id = self.generate_session_id()
        
        # Create session
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            message_count=0,
            is_active=True,
            metadata=metadata or {}
        )
        
        # Store session and initialize conversation
        self.sessions[session_id] = session
        self.conversations[session_id] = []
        
        logger.info(f"Created new session {session_id} for user {user_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def is_session_valid(self, session_id: str) -> bool:
        """Check if a session is valid and not expired."""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Check if session is active
        if not session.is_active:
            return False
        
        # Check if session has expired
        timeout_threshold = datetime.now() - timedelta(hours=self.session_timeout_hours)
        if session.last_activity < timeout_threshold:
            session.is_active = False
            return False
        
        return True
    
    def add_message(self, session_id: str, user_id: str, message: str, response: str, 
                   agent_used: Optional[str] = None, routing_reason: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a message to a session's conversation history.
        
        Args:
            session_id: Session ID
            user_id: User ID
            message: User's message
            response: AI response
            agent_used: Which agent was used
            routing_reason: Why the agent was chosen
            metadata: Additional metadata
            
        Returns:
            Message ID
        """
        # Validate session
        if not self.is_session_valid(session_id):
            raise ValueError(f"Invalid or expired session: {session_id}")
        
        # Generate message ID
        message_id = f"msg_{uuid.uuid4().hex[:12]}"
        
        # Create chat message
        chat_message = ChatMessage(
            message_id=message_id,
            user_id=user_id,
            session_id=session_id,
            message=message,
            response=response,
            agent_used=agent_used,
            routing_reason=routing_reason,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Add to conversation history
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append(chat_message)
        
        # Update session
        session = self.sessions[session_id]
        session.last_activity = datetime.now()
        session.message_count += 1
        
        logger.info(f"Added message {message_id} to session {session_id}")
        return message_id
    
    def get_conversation_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of messages to return (None for all)
            
        Returns:
            List of message dictionaries
        """
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]
        
        # Convert to dictionaries
        message_dicts = [asdict(msg) for msg in messages]
        
        # Apply limit if specified
        if limit:
            message_dicts = message_dicts[-limit:]
        
        return message_dicts
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user."""
        user_sessions = []
        
        for session in self.sessions.values():
            if session.user_id == user_id:
                session_dict = asdict(session)
                session_dict['conversation_count'] = len(self.conversations.get(session.session_id, []))
                user_sessions.append(session_dict)
        
        return user_sessions
    
    def end_session(self, session_id: str) -> bool:
        """End a session (mark as inactive)."""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            logger.info(f"Ended session {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions."""
        current_time = datetime.now()
        timeout_threshold = current_time - timedelta(hours=self.session_timeout_hours)
        
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.last_activity < timeout_threshold:
                expired_sessions.append(session_id)
        
        # Remove expired sessions
        for session_id in expired_sessions:
            del self.sessions[session_id]
            if session_id in self.conversations:
                del self.conversations[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about all sessions."""
        total_sessions = len(self.sessions)
        active_sessions = sum(1 for s in self.sessions.values() if s.is_active)
        total_messages = sum(len(conv) for conv in self.conversations.values())
        
        # Get unique users
        unique_users = set(session.user_id for session in self.sessions.values())
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_messages": total_messages,
            "unique_users": len(unique_users),
            "session_timeout_hours": self.session_timeout_hours
        }
    
    def export_session_data(self, session_id: str) -> Dict[str, Any]:
        """Export session data for backup or analysis."""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        return {
            "session": asdict(session),
            "conversation": self.get_conversation_history(session_id)
        }

# Global session manager instance
session_manager = SessionManager() 