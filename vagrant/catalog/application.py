#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Home page"


@app.route("/catalog/<int:category_id>/", methods=["POST"])
def add_item():
    return "Adding Item"


@app.route("/catalog/<int:category_id>/", methods=["GET"])
def list_items():
    return "Listing Items"


@app.route("/catalog/<int:category_id>/<int:item_id>", methods=["DELETE"])
def delete_item():
    return "Deleting Item"


@app.route("/catalog/login", methods=["POST"])
def login():
    return "Login"

# import psycopg2

# with psycopg2.connect("dbname=catalog") as db:

#     cur = db.cursor()

#     query1 = ("select * from categories;")
#     cur.execute(query1)
#     for register in cur.fetchall():
#         print register[0]
