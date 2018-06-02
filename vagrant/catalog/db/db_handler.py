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

    def insert_item(self, title, description, category):
        item = Item(title=title, description=description,
                    category=self._get_category(category))
        self.session.add(item)
        self.session.commit()

    def list_categories(self):
        return self.session.query(Category).all()

    def delete_item(self, item_id):
        item = self.session.query(Item).filter_by(id=item_id).one()
        print "item", item
        self.session.delete(item)
        self.session.commit()

    def get_category_name(self, category_id):
        return self.session.query(Category).filter_by(id=category_id).one().title

    def _get_category(self, category_id):
        return self.session.query(Category).filter_by(id=category_id).one()

    def get_item(self, item_id):
        return self.session.query(Item).filter_by(id=item_id).one()