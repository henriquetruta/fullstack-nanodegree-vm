#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, render_template, url_for
from db.db_handler import Database
app = Flask(__name__)

db = Database()

@app.route("/catalog")
@app.route("/")
def home():
    categories = db.list_categories()
    latest = db.get_latest_items()
    return render_template('home.html', categories=categories,
                           latest=latest)


@app.route("/catalog/item/new", methods=["POST", "GET"])
def add_item():
    if request.method == 'POST':
        category = request.form['category']
        db.insert_item(request.form['name'],
                       request.form['description'],
                       category)
        return redirect(url_for('list_items', category_name=category))
    else:
        categories = db.list_categories()
        return render_template('new_item.html', categories=categories)


@app.route("/catalog/<category_name>/<item_name>/details", methods=["GET"])
def get_item(category_name, item_name):
    item = db.get_item(item_name, category_name)
    return render_template('item_description.html', item=item)


@app.route("/catalog/<category_name>/list", methods=["GET"])
def list_items(category_name):
    items = db.list_items(category_name)
    category_name = db.get_category_name(category_name)
    return render_template('items.html', items=items,
                           category_name=category_name)


@app.route("/catalog/<category_name>/item/<item_name>/delete", methods=["POST", "GET"])
def delete_item(item_name, category_name):
    item = db.get_item(item_name, category_name)
    if request.method == 'POST':
        db.delete_item(item_name, category_name)
        return redirect(url_for('list_items', category_name=item.categoryName))
    else:
        return render_template('item_delete.html', item=item)


@app.route("/catalog/<category_name>/item/<item_name>/edit", methods=["POST", "GET"])
def edit_item(category_name, item_name):
    item = db.get_item(item_name, category_name)
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.categoryName = request.form['category']
        db.edit_item(item)
        return redirect(url_for('get_item', item_name=item.name,
                        category_name=category_name))
    else:
        categories = db.list_categories()
        return render_template('item_edit.html', item=item,
                               categories=categories)


@app.route("/catalog/login", methods=["POST"])
def login():
    return "Login"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, use_debugger=True)


# TODO:
# Login
# Check if the user created
# Bug: Change category
# JSON
# HTML
# CSS