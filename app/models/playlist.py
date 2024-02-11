from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Playlist(BaseModel):
  playlistID: str = None
  title: str = None
  description: str = None
  userID: str = None
  dateTimeCreated: datetime = None
  dateTimeModified: datetime = None
  songs: Optional[List[str]] = None