#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, flash, jsonify, make_response, redirect, request
from flask import render_template, url_for
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
import random
import requests
import string

from db.db_handler import Database

app = Flask(__name__)
app.secret_key = 'some secret key'

# Creates an instance of the Database handler
db = Database()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


@app.route("/catalog")
@app.route("/")
def home():
    categories = db.list_categories()
    latest = db.get_latest_items()
    return render_template('home.html', categories=categories,
                           latest=latest)


@app.route("/catalog.json")
def items_json():
    items = db.list_all_items_json()
    return jsonify(Items=[i.serialize for i in items])


@app.route("/catalog/item/new", methods=["POST", "GET"])
def add_item():
    if request.method == 'POST':
        category = request.form['category']
        db.insert_item(request.form['name'],
                       request.form['description'],
                       category,
                       login_session['email'])
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
    categories = db.list_categories()
    return render_template('items.html', items=items, amount=len(items),
                           categories=categories, category_name=category_name)


@app.route("/catalog/<category_name>/item/<item_name>/delete",
           methods=["POST", "GET"])
def delete_item(item_name, category_name):
    item = db.get_item(item_name, category_name)
    if request.method == 'POST':
        db.delete_item(item_name, category_name)
        return redirect(url_for('list_items', category_name=item.categoryName))
    else:
        return render_template('item_delete.html', item=item)


@app.route("/catalog/<category_name>/item/<item_name>/edit",
           methods=["POST", "GET"])
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
                        category_name=item.categoryName))
    else:
        categories = db.list_categories()
        return render_template('item_edit.html', item=item,
                               categories=categories)


@app.route("/catalog/login", methods=["GET"])
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Connects to Google oauth API."""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['logged_in'] = True

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output


@app.route('/logout')
def logout():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['logged_in']
        flash("Successfully logged out!")
        return home()
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, use_debugger=True)
