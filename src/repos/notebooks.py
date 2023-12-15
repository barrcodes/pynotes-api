from sqlalchemy.orm import Session
from .base import BaseRepository
from src.models.notebook import Notebook
from src.schemas.notebook import NotebookCreate, NotebookUpdate

class NotebookRepo(BaseRepository[Notebook, NotebookCreate, NotebookUpdate]):
    def __init__(self, db: Session):
        super().__init__(Notebook, db)
