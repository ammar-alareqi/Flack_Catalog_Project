from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, User, Category, Item
import datetime

engine = create_engine('sqlite:///cafemenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Menu Items:
# 1. Coffe menu items:
category_coffee = Category(name = 'Coffee')

session.add(category_coffee)
session.commit()

citem1 = Item(name = 'Italian Coffee', description = 'Good Italian coffee',
                date = datetime.datetime.now(), category = category_coffee)

session.add(citem1)
session.commit()

citem2 = Item(name = 'Frensh Coffee', description = 'Good Frensh coffee',
                date = datetime.datetime.now(), category = category_coffee)

session.add(citem2)
session.commit()

citem3 = Item(name = 'Turkish Coffee', description = 'Good Turkish coffee',
                date = datetime.datetime.now(), category = category_coffee)

session.add(citem3)
session.commit()

citem4 = Item(name = 'American Coffee', description = 'Good American coffee',
                date = datetime.datetime.now(), category = category_coffee)

session.add(citem4)
session.commit()

# 2. Tea menu items:
category_tea = Category(name = 'Tea')

session.add(category_tea)
session.commit()

titem1 = Item(name = 'Green Tea', description = 'Good Green Tea',
                date = datetime.datetime.now(), category = category_tea)

session.add(titem1)
session.commit()

titem2 = Item(name = 'Black Tea', description = 'Good Black Tea',
                date = datetime.datetime.now(), category = category_tea)

session.add(titem2)
session.commit()

titem3 = Item(name = 'White Tea', description = 'Good White Tea',
                date = datetime.datetime.now(), category = category_tea)

session.add(titem3)
session.commit()

# 3. Juice menu items:
category_juice = Category(name = 'Juice')

session.add(category_juice)
session.commit()

jitem1 = Item(name = 'Orang Juice', description = 'Good Orang Juice',
                date = datetime.datetime.now(), category = category_juice)

session.add(jitem1)
session.commit()

jitem2 = Item(name = 'Mango Juice', description = 'Good Mango Juice',
                date = datetime.datetime.now(), category = category_juice)

session.add(jitem2)
session.commit()

jitem3 = Item(name = 'Apple Juice', description = 'Good Apple Juice',
                date = datetime.datetime.now(), category = category_juice)

session.add(jitem3)
session.commit()