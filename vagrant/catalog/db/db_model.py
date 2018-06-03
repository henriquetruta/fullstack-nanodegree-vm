import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(250), nullable=False)
    categoryId = Column(Integer, ForeignKey('category.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    category = relationship(Category)