from fastapi import APIRouter, Body, Response, Depends
from sqlalchemy.orm import Session
from src.repos.notebooks import NotebookRepo
from src.repos.categories import CategoryRepo
from src.repos.db import get_db
from src.repos.notes import NoteRepo
from src.schemas.note import NoteCreate, NoteUpdate
from src.exceptions.notfound import NotFoundException

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_notes(notebook_id: int, db: Session = Depends(get_db)):
    notes = NoteRepo(db)
    notebooks = NotebookRepo(db)
    # throws on failed get - important because this particular call has no simpler way to guarantee notebook_id is valid
    notebooks.get(notebook_id)
    return notes.get_all(notebook_id)

@router.get("/{note_id}")
def get_note(notebook_id: int, note_id: int, db: Session = Depends(get_db)):
    notes = NoteRepo(db)
    return notes.get(notebook_id, note_id)

@router.post("/")
def create_note(notebook_id: int, note: NoteCreate = Body(...), db: Session = Depends(get_db)):
    notes = NoteRepo(db)
    categories = CategoryRepo(db)
    # throws on failed get - important because this particular call has no simpler way to guarantee notebook_id is valid
    categories.get(notebook_id, note.category_id)
    note = notes.create(note)
    db.commit()
    db.refresh(note)
    return note

@router.put("/{note_id}")
def update_note(notebook_id: int, note_id: int, note: NoteUpdate = Body(...), db: Session = Depends(get_db)):
    notes = NoteRepo(db)
    note = notes.update(notebook_id, note_id, note)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(notebook_id: int, note_id: int, db: Session = Depends(get_db)):
    notes = NoteRepo(db)
    notes.delete(notebook_id, note_id)
    db.commit()
    return Response(content='', status_code=200)
