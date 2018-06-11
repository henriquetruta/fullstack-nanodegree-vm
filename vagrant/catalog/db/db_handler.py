from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Category, Item


class Database():
    """Abstraction layer for database"""

    def __init__(self):
        """Creates the necessary objects to connect to the postgres DB"""
        engine = create_engine('postgresql:///catalog')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def list_items(self, category):
        """Lists all items in a given category"""
        return self.session.query(Item).filter_by(categoryName=category).all()

    def list_all_items(self):
        """Lists all items in the database"""
        return self.session.query(Item).all()

    def get_latest_items(self):
        """Lists the 10 latest added items"""
        return self.session.query(Item).order_by(
            Item.created_date.desc()).limit(10).all()

    def insert_item(self, name, description, category, email):
        """Inserts an item in the database"""
        item = Item(name=name, description=description,
                    category=self._get_category(category),
                    created_by=email)
        self.session.add(item)
        self.session.commit()

    def list_categories(self):
        """Lists all categories in the database"""
        return self.session.query(Category).all()

    def delete_item(self, item_name, category_name):
        """Deletes an item from the database"""
        item = self.session.query(Item).filter_by(
            name=item_name, categoryName=category_name).one()
        self.session.delete(item)
        self.session.commit()

    def edit_item(self, item):
        """Edits an item from the database"""
        self.session.add(item)
        self.session.commit()

    def _get_category(self, category_name):
        """Gets a category object from the database (helper method)"""
        return self.session.query(Category).filter_by(
            name=category_name).one()

    def get_item(self, item_name, category_name):
        """Gets an item object from the database"""
        return self.session.query(Item).filter_by(
            name=item_name, categoryName=category_name).one()
