from pydantic import BaseModel
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    category_id: int
    pass

class NoteUpdate(NoteBase):
    category_id: Optional[int] = None
    pinned: Optional[int] = None
    pass