from typing import List
from sqlalchemy.orm import Session

from src.exceptions.notfound import NotFoundException
from .base import BaseRepository
from src.models.notebook import Category
from src.schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepo(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self, db: Session):
        super().__init__(Category, db)
    
    def get_all(self, notebook_id: int) -> List[Category]:
        return self.db.query(self.model).filter(self.model.notebook_id == notebook_id).all()
    
    def get(self, notebook_id: int, id: int) -> Category:
        db_obj = self.db.query(Category).filter((Category.id == id) & (Category.notebook_id == notebook_id)).first()
        if db_obj is None:
            raise NotFoundException(f'{id} not found')
        return db_obj
    
    def create(self, notebook_id: int, obj: CategoryCreate) -> Category:
        db_obj = Category(**obj.model_dump())
        db_obj.notebook_id = notebook_id
        self.db.add(db_obj)
        return db_obj
    
    def update(self, notebook_id: int, id: int, obj: CategoryUpdate) -> Category:
        db_obj = self.get(notebook_id, id)
        for key, value in obj:
            setattr(db_obj, key, value)
        return db_obj
    
    def delete(self, notebook_id: int, id: int) -> Category:
        db_obj = self.get(notebook_id, id)
        self.db.delete(db_obj)
        return None
