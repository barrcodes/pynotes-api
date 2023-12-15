from pydantic import BaseModel

class NotebookBase(BaseModel):
    name: str

class NotebookCreate(NotebookBase):
    pass

class NotebookUpdate(NotebookBase):
    pass
