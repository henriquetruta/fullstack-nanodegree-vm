import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_model import Category, Item, Base

engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

football = Category(name="Football")
baseball = Category(name="Baseball")
frisbee = Category(name="Frisbee")
snowboarding = Category(name="Snowboarding")
rock_climbing = Category(name="Rock Climbing")
foosball = Category(name="Foosball")
skating = Category(name="Skating")
hockey = Category(name="Hockey")
categories = [football, baseball, frisbee, snowboarding, rock_climbing,
            foosball, skating, hockey]
session.bulk_save_objects(categories)

football_shoes = Item(name="Shoe", description="very cool",
                      categoryName="Football", created_by='henrique')
football_ball = Item(name="Ball", description="Nice ball",
                      categoryName="Football", created_by='henrique')
baseball_ball = Item(name="Ball", description="Best ever",
                      categoryName="Baseball", created_by='henrique')
items = [football_shoes, football_ball, baseball_ball]

session.bulk_save_objects(items)
session.commit()
