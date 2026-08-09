from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import uuid

from .database import get_db
from .crud import CRUDOperations

class ChatHistoryManager:
    def __init__(self):
        self.db = next(get_db())
    
    def save_message(self, session_id: str, message: Dict[str, Any]):
        """Save a message to chat history in MySQL"""
        # Check if session exists, if not create it
        session = CRUDOperations.get_session(self.db, session_id)
        if not session:
            CRUDOperations.create_session(self.db, session_id)
        
        # Save message
        CRUDOperations.save_chat_message(
            db=self.db,
            session_id=session_id,
            role=message['role'],
            content=message['content'],
            evaluation=message.get('evaluation'),
            hallucination_check=message.get('hallucination_check'),
            sources=message.get('sources'),
            tool_calls=message.get('tool_calls')
        )
    
    def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history from MySQL"""
        messages = CRUDOperations.get_chat_history(self.db, session_id, limit)
        
        # Convert to dict format
        result = []
        for msg in messages:
            result.append({
                'role': msg.role,
                'content': msg.content,
                'evaluation': msg.evaluation,
                'hallucination_check': msg.hallucination_check,
                'sources': msg.sources,
                'tool_calls': msg.tool_calls,
                'timestamp': msg.created_at.isoformat() if msg.created_at else None
            })
        
        return result[::-1]  # Reverse to chronological order
    
    def clear_chat_history(self, session_id: str):
        """Clear chat history for a session"""
        # Delete all messages for session
        self.db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).delete()
        self.db.commit()
    
    def get_all_sessions(self) -> List[str]:
        """Get all session IDs"""
        sessions = self.db.query(Session.session_id).filter(
            Session.is_active == True
        ).all()
        return [s[0] for s in sessions]