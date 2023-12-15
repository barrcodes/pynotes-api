from typing import Callable, List, TypeVar, Generic, Type, Optional
from sqlalchemy.orm import Session
from src.exceptions.notfound import NotFoundException
from typing import Union

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if db_obj is None:
            raise NotFoundException(f'{id} not found')
        return db_obj

    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    def create(self, obj: CreateSchemaType) -> ModelType:
        print(obj.model_dump())
        db_obj = self.model(**obj.model_dump())
        self.db.add(db_obj)
        return db_obj

    def update(self, id: int, obj: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if db_obj is None:
            raise NotFoundException(f'{id} not found')
        for key, value in obj:
            setattr(db_obj, key, value)
        return db_obj

    def delete(self, id: int) -> Optional[ModelType]:
        db_obj = self.get(id)
        self.db.delete(db_obj)
        return None