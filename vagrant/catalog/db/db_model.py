import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(250),primary_key=True)

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(64), primary_key=True)
    categoryName = Column(String, ForeignKey('category.name'), primary_key=True)
    description = Column(String(250), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(64))
    category = relationship(Category)