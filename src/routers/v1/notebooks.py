from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.orm import Session, joinedload
from src.models.notebook import Notebook
from src.repos.db import get_db
from .categories import router as categories_router
from .notes import router as notes_router
from src.repos.notebooks import NotebookRepo
from src.schemas.notebook import NotebookCreate, NotebookUpdate
from src.exceptions.notfound import NotFoundException

router = APIRouter(
    prefix="/notebooks",
    tags=["notebooks"],
    responses={404: {"description": "Not found"}},
)

router.include_router(categories_router, prefix="/{notebook_id}")
router.include_router(notes_router, prefix="/{notebook_id}")

@router.get("/")
def get_notebooks(db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    return notebooks.get_all()

@router.get("/{notebook_id}")
def get_notebook(notebook_id: int, db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    notebook = notebooks.get(notebook_id)
    db.query(Notebook).options(joinedload(Notebook.categories)).filter(Notebook.id == notebook_id).all()
    return notebook

@router.post("/")
def create_notebook(notebook_input: NotebookCreate = Body(...), db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    notebook_output = notebooks.create(notebook_input)
    db.commit()
    db.refresh(notebook_output)
    return notebook_output

@router.put("/{notebook_id}")
def update_notebook(notebook_id: int, notebook_input: NotebookUpdate = Body(...), db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    notebook_output = notebooks.update(notebook_id, notebook_input)
    db.commit()
    db.refresh(notebook_output)
    return notebook_output


@router.delete("/{notebook_id}")
def delete_notebook(notebook_id: int, db: Session = Depends(get_db)):
    notebooks = NotebookRepo(db)
    notebooks.delete(notebook_id)
    db.commit()
    return Response(content='', status_code=200)
