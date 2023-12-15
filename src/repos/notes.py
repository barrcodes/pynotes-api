from typing import List, Optional, Union
from sqlalchemy.orm import Session

from src.exceptions.notfound import NotFoundException
from .base import BaseRepository
from src.models.notebook import Category, Note
from src.schemas.note import NoteCreate, NoteUpdate

class NoteRepo(BaseRepository[Note, NoteCreate, NoteUpdate]):
    def __init__(self, db: Session):
        super().__init__(Note, db)

    def get_all(self, notebook_id: int) -> List[Note]:
        return self.db.query(Note).join(Category).filter(Category.notebook_id == notebook_id).all()
    
    def get(self, notebook_id: int, id: int) -> Note:
        db_obj = self.db.query(Note).join(Category).filter((Note.id == id) & (Category.notebook_id == notebook_id)).first()
        if db_obj is None:
            raise NotFoundException(f'{id} not found')
        return db_obj
    
    # no create, category is referenced by CreateSchema, and category is validated in router
    
    def update(self, notebook_id: int, id: int, obj: NoteUpdate) -> Note:
        db_obj = self.get(notebook_id, id)
        if (obj.category_id is None):
            obj.category_id = db_obj.category_id
        if (obj.pinned is None):
            obj.pinned = db_obj.pinned
        return super().update(id, obj)
    
    def delete(self, notebook_id: int, id: int) -> Note:
        db_obj = self.get(notebook_id, id)
        self.db.delete(db_obj)
        return None
