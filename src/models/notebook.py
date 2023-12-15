from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Notebook(Base):
    __tablename__ = 'notebooks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    categories = relationship('Category', backref='notebook')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Notebook: {self.name}>'

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    notebook_id = Column(Integer, ForeignKey('notebooks.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    parent = relationship('Category', remote_side=[id])
    notes = relationship('Note', backref='category')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name: str, parent_id: Optional[int] = None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return f'<Category: {self.name}>'

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    pinned = Column(Integer, default=None, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, category_id: int, title: str, content: str):
        self.category_id = category_id
        self.title = title
        self.content = content
