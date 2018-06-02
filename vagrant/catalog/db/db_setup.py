import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_model import Category, Item, Base

engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

football = Category(title="Football")
baseball = Category(title="Baseball")
frisbee = Category(title="Frisbee")
snowboarding = Category(title="Snowboarding")
rock_climbing = Category(title="Rock Climbing")
foosball = Category(title="Foosball")
skating = Category(title="Skating")
hockey = Category(title="Hockey")
categories = [football, baseball, frisbee, snowboarding, rock_climbing,
            foosball, skating, hockey]
session.bulk_save_objects(categories)

football_shoes = Item(title="Shoe", description="very cool",
                      categoryId=1)
football_ball = Item(title="Ball", description="Nice ball",
                      categoryId=1)
baseball_ball = Item(title="Ball", description="Best ever",
                      categoryId=2)
items = [football_shoes, football_ball, baseball_ball]

session.bulk_save_objects(items)
session.commit()
