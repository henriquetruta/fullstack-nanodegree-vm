from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Category, Item


class Database():
    def __init__(self):
        engine = create_engine('postgresql:///catalog')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def list_items(self, category):
        return self.session.query(Item).filter_by(categoryName=category).all()

    def list_all_items_json(self):
        return self.session.query(Item).all()

    def get_latest_items(self):
        return self.session.query(Item).order_by(
            Item.created_date.desc()).limit(10).all()

    def insert_item(self, name, description, category, email):
        item = Item(name=name, description=description,
                    category=self._get_category(category),
                    created_by=email)
        self.session.add(item)
        self.session.commit()

    def list_categories(self):
        return self.session.query(Category).all()

    def delete_item(self, item_name, category_name):
        item = self.session.query(Item).filter_by(
            name=item_name, categoryName=category_name).one()
        self.session.delete(item)
        self.session.commit()

    def edit_item(self, item):
        self.session.add(item)
        self.session.commit()

    def get_category_name(self, category_name):
        return self.session.query(Category).filter_by(
            name=category_name).one().name

    def _get_category(self, category_name):
        return self.session.query(Category).filter_by(
            name=category_name).one()

    def get_item(self, item_name, category_name):
        return self.session.query(Item).filter_by(
            name=item_name, categoryName=category_name).one()
