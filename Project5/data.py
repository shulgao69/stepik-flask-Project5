import csv

from models import Category, db, Meal
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wdmaolxqzifxaw:6ea24e7a7f23fbcbd77b6fbe0e53237faaa06f5df90939c52144cb416a2b27ad@ec2-54-211-55-24.compute-1.amazonaws.com:5432/d3p4mvv6o99bef'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

with open("delivery_categories.csv", "r", encoding="utf-8") as ff:
    delivery_categories = csv.DictReader(ff, delimiter=',')
    for categories in delivery_categories:
        category = Category(id = categories["id"], title = categories["title"])
        db.session.add(category)
db.session.commit()

with open("delivery_items.csv", "r", encoding="utf-8") as f_obj:
    delivery_items = csv.DictReader(f_obj, delimiter=',')

    for items in delivery_items:
        meal = Meal(id = items["id"], title = items["title"], price = items["price"],
                    description = items["description"], picture = items["picture"], categories_id = items["category_id"])
        db.session.add(meal)
db.session.commit()

