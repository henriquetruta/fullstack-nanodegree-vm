#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from db.db_handler import Database
app = Flask(__name__)

db = Database()

@app.route("/")
def home():
    cats = db.list_categories()
    return render_template('home.html', categories=cats)

@app.route("/catalog/<int:category_id>/", methods=["POST"])
def add_item():
    return "Adding Item"


@app.route("/catalog/<int:category_id>/list", methods=["GET"])
def list_items(category_id):
    items = db.list_items(category_id)
    category_name = db.get_category_name(category_id)
    print len(items)
    print category_name
    return render_template('items.html', items=items,
                           category_name=category_name)


@app.route("/catalog/<int:category_id>/<int:item_id>", methods=["DELETE"])
def delete_item():
    return "Deleting Item"


@app.route("/catalog/login", methods=["POST"])
def login():
    return "Login"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, use_debugger=True)
