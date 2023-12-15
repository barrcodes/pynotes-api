from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.orm import Session
from src.repos.db import get_db
from src.models.notebook import Category
from src.repos.categories import CategoryRepo
from src.repos.notebooks import NotebookRepo
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.exceptions.notfound import NotFoundException
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_categories(notebook_id: int, db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    categories = CategoryRepo(db)
    # throws on failed get - important because this particular call has no simpler way to guarantee notebook_id is valid
    notebooks.get(notebook_id)
    return categories.get_all(notebook_id)



@router.get("/{category_id}")
def get_category(notebook_id: int, category_id: int, db: Session = Depends(get_db)):
    categories = CategoryRepo(db)
    return categories.get(notebook_id, category_id)

@router.post("/")
def create_category(notebook_id: int, category_input: CategoryCreate = Body(...), db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    categories = CategoryRepo(db)
    # throws on failed get - important because this particular call has no simpler way to guarantee notebook_id is valid
    notebooks.get(notebook_id)
    category_output = categories.create(notebook_id, category_input)
    db.commit()
    db.refresh(category_output)
    return category_output

@router.put("/{category_id}")
def update_category(notebook_id:int, category_id: int, category_input: CategoryUpdate = Body(...), db: Session = Depends(get_db)):
    categories = CategoryRepo(db)
    category_output = categories.update(notebook_id, category_id, category_input)
    db.commit()
    db.refresh(category_output)
    return category_output

@router.delete("/{category_id}")
def delete_category(notebook_id: int, category_id: int, db: Session = Depends(get_db)):
    categories = CategoryRepo(db)
    categories.delete(notebook_id, category_id)
    db.commit()
    return Response(content='', status_code=200)
