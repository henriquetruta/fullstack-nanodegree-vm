from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Category, Item

class Database():
    def __init__(self):
        engine = create_engine('postgresql:///catalog')
        Base.metadata.bind=engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def list_items(self, category):
        return self.session.query(Item).filter_by(categoryId=category).all()

    def list_categories(self):
        return self.session.query(Category).all()

    def get_category_name(self, category_id):
        return self.session.query(Category).filter_by(id=category_id).one().title