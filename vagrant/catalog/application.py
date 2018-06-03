#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, render_template, url_for
from db.db_handler import Database
app = Flask(__name__)

db = Database()

@app.route("/")
def home():
    categories = db.list_categories()
    latest = db.get_latest_items()
    return render_template('home.html', categories=categories,
                           latest=latest)


@app.route("/item/new", methods=["POST", "GET"])
def add_item():
    if request.method == 'POST':
        category = request.form['category']
        db.insert_item(request.form['title'],
                       request.form['description'],
                       category)
        return redirect(url_for('list_items', category_id=category))
    else:
        categories = db.list_categories()
        return render_template('new_item.html', categories=categories)


@app.route("/catalog/<int:item_id>/details", methods=["GET"])
def get_item(item_id):
    item = db.get_item(item_id)
    return render_template('item_description.html', item=item)


@app.route("/catalog/<int:category_id>/list", methods=["GET"])
def list_items(category_id):
    items = db.list_items(category_id)
    category_name = db.get_category_name(category_id)
    return render_template('items.html', items=items,
                           category_name=category_name)


@app.route("/item/<int:item_id>/delete", methods=["POST", "GET"])
def delete_item(item_id):
    item = db.get_item(item_id)
    if request.method == 'POST':
        db.delete_item(item_id)
        return redirect(url_for('list_items', category_id=item.categoryId))
    else:
        return render_template('item_delete.html', item=item)


@app.route("/item/<int:item_id>/edit", methods=["POST", "GET"])
def edit_item(item_id):
    print "YAYY"
    item = db.get_item(item_id)
    if request.method == 'POST':
        print "YAYY2"
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.categoryId = request.form['category']
        print "YAYY3"
        db.edit_item(item)
        return redirect(url_for('get_item', item_id=item.id))
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
# Latest items
# Redo URLs
# Login
# Check if the user created
# HTML
# CSS