import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for handling database operations with Supabase"""
    
    def __init__(self):
        # Supabase configuration
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials not found. Using in-memory storage.")
            self.supabase = None
            self._in_memory_storage = {}
        else:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            self._in_memory_storage = None
    
    async def create_meeting(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new meeting record in the database
        
        Args:
            meeting_data: Dictionary containing meeting information
            
        Returns:
            Dict: Created meeting record
        """
        try:
            if self.supabase:
                # Insert into Supabase
                response = self.supabase.table("meetings").insert(meeting_data).execute()
                return response.data[0] if response.data else meeting_data
            else:
                # Store in memory
                meeting_id = meeting_data["id"]
                self._in_memory_storage[meeting_id] = meeting_data
                return meeting_data
                
        except Exception as e:
            logger.error(f"Error creating meeting: {str(e)}")
            raise Exception(f"Failed to create meeting record: {str(e)}")
    
    async def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a meeting record by ID
        
        Args:
            meeting_id: Unique identifier for the meeting
            
        Returns:
            Dict: Meeting record or None if not found
        """
        try:
            if self.supabase:
                # Query Supabase
                response = self.supabase.table("meetings").select("*").eq("id", meeting_id).execute()
                return response.data[0] if response.data else None
            else:
                # Get from memory
                return self._in_memory_storage.get(meeting_id)
                
        except Exception as e:
            logger.error(f"Error retrieving meeting {meeting_id}: {str(e)}")
            return None
    
    async def update_meeting_status(self, meeting_id: str, status: str, error_message: Optional[str] = None) -> bool:
        """
        Update the status of a meeting
        
        Args:
            meeting_id: Unique identifier for the meeting
            status: New status
            error_message: Optional error message if status is failed
            
        Returns:
            bool: Success status
        """
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.now().isoformat()
            }
            
            if error_message:
                update_data["error_message"] = error_message
            
            if self.supabase:
                # Update in Supabase
                response = self.supabase.table("meetings").update(update_data).eq("id", meeting_id).execute()
                return len(response.data) > 0
            else:
                # Update in memory
                if meeting_id in self._in_memory_storage:
                    self._in_memory_storage[meeting_id].update(update_data)
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error updating meeting status: {str(e)}")
            return False
    
    async def update_meeting_results(self, meeting_id: str, results: Dict[str, Any]) -> bool:
        """
        Update meeting with analysis results
        
        Args:
            meeting_id: Unique identifier for the meeting
            results: Dictionary containing transcript, summary, action_items, key_decisions
            
        Returns:
            bool: Success status
        """
        try:
            update_data = {
                "transcript": results.get("transcript"),
                "summary": results.get("summary"),
                "action_items": results.get("action_items", []),
                "key_decisions": results.get("key_decisions", []),
                "status": results.get("status"),
                "updated_at": datetime.now().isoformat()
            }
            
            if self.supabase:
                # Update in Supabase
                response = self.supabase.table("meetings").update(update_data).eq("id", meeting_id).execute()
                return len(response.data) > 0
            else:
                # Update in memory
                if meeting_id in self._in_memory_storage:
                    self._in_memory_storage[meeting_id].update(update_data)
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error updating meeting results: {str(e)}")
            return False
    
    async def get_meetings(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get list of meetings with pagination
        
        Args:
            limit: Number of meetings to return
            offset: Number of meetings to skip
            
        Returns:
            List: List of meeting records
        """
        try:
            if self.supabase:
                # Query Supabase with pagination
                response = self.supabase.table("meetings").select("*").order("created_at", desc=True).range(offset, offset + limit - 1).execute()
                return response.data
            else:
                # Get from memory with pagination
                meetings = list(self._in_memory_storage.values())
                meetings.sort(key=lambda x: x.get("created_at", ""), reverse=True)
                return meetings[offset:offset + limit]
                
        except Exception as e:
            logger.error(f"Error retrieving meetings: {str(e)}")
            return []
    
    async def delete_meeting(self, meeting_id: str) -> bool:
        """
        Delete a meeting record
        
        Args:
            meeting_id: Unique identifier for the meeting
            
        Returns:
            bool: Success status
        """
        try:
            if self.supabase:
                # Delete from Supabase
                response = self.supabase.table("meetings").delete().eq("id", meeting_id).execute()
                return len(response.data) > 0
            else:
                # Delete from memory
                if meeting_id in self._in_memory_storage:
                    del self._in_memory_storage[meeting_id]
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error deleting meeting: {str(e)}")
            return False
    
    async def create_tables(self):
        """
        Create necessary tables in Supabase (run once during setup)
        """
        if not self.supabase:
            logger.info("Skipping table creation - using in-memory storage")
            return
        
        try:
            # This would typically be done via Supabase dashboard or migrations
            # For now, we'll just log that tables should be created
            logger.info("""
            Please create the following table in your Supabase dashboard:
            
            CREATE TABLE meetings (
                id UUID PRIMARY KEY,
                title TEXT NOT NULL,
                filename TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                transcript TEXT,
                summary TEXT,
                action_items JSONB DEFAULT '[]',
                key_decisions JSONB DEFAULT '[]',
                error_message TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            CREATE INDEX idx_meetings_created_at ON meetings(created_at DESC);
            CREATE INDEX idx_meetings_status ON meetings(status);
            """)
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}") 