from flask import Flask, render_template, request, redirect, jsonify, url_for, flash 
from sqlalchemy import create_engine, asc, desc 
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item
import datetime

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Cafe Application"


engine = create_engine('sqlite:///cafemenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    return render_template('catalog.html', categories=categories, items=items)
    #return render_template('catalog.html')


@app.route('/catalog/category/')
def showCategory():
    # add your code
    # return render_template('categories.html')
    pass


@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(
        desc(Item.date))
    return render_template('items.html', items = items)


@app.route('/catalog/<int:item_id>/item_description/')
def showSelectedItem(item_id):
    selectedItem = session.query(Item).filter_by(id=item_id).all()
    return render_template('item_description.html', item = selectedItem)


@app.route('/catalog/user/')
def showCatalogUser():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    if 'username' in login_session:
        return render_template('catalog_user.html',
        categories=categories, items=items)
    else:
        return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/<int:category_id>/items/user/')
def showItemsUser(category_id):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).order_by(
        desc(Item.date))
    if 'username' in login_session:
        return render_template('items_user.html', items = items)
    else:
        return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/<int:item_id>/item_description/user/')
def showSelectedItemUser(item_id):
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    if 'username' in login_session:
        selectedItem = session.query(Item).filter_by(id=item_id).all()
        return render_template('item_description_user.html',
        item = selectedItem)
    else:
        return render_template('catalog.html', categories=categories,
        items=items)


@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    if 'username' in login_session:
        if request.method == 'POST':
            newitem = Item(
                name=request.form['name'], 
                description=request.form['description'],
                date=datetime.datetime.now(),
                category=session.query(Category).filter_by(
                                id=request.form['category']).one(),
                user_id = login_session['email'])
            session.add(newitem)
            session.commit()
            flash('A new item was added!')
            return redirect(url_for('showCatalogUser'))
        else:
            return render_template('add.html', categories=categories)
    else:
        return redirect(url_for('showCatalogUser', categories=categories,
        items=items))


@app.route('/catalog/<int:itemid>/edit/', methods=['GET', 'POST'])
def editItem(itemid):
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    item = session.query(Item).filter_by(id=itemid).one()
    if 'username' not in login_session:
        return redirect(url_for('login'))
    elif item.user_id == login_session['email']:
        categories = session.query(Category).all()
        if request.method == 'POST':
            item.name = request.form['name']
            item.description = request.form['description']
            item.category=session.query(Category).filter_by(
                                id=request.form['category']).one()
            item.date = datetime.datetime.now()
            session.add(item)
            session.commit()
            flash('Item was edited successfully!')
            return redirect(url_for('showCatalogUser'))
        else:
            return render_template('edit.html',categories=categories, item=item)
    else:
        # return redirect(url_for('showCatalogUser'))
        return redirect(url_for('showCatalog', categories=categories,
        items=items))


@app.route('/catalog/<int:itemid>/delete/', methods=['GET', 'POST'])
def deleteItem(itemid):
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.date)).limit(4)
    item = session.query(Item).filter_by(id=itemid).one()
    if 'username' not in login_session:
        return redirect(url_for('login'))
    elif item.user_id == login_session['email']:
        categories = session.query(Category).all()
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            flash('Item has been deleted')
            return redirect(url_for('showCatalogUser'))
        else:
            return render_template('delete.html', item=item)
    else:
        return redirect(url_for('showCatalog', categories=categories,
        items=items))



@app.route('/catalog/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
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
    g_id = credentials.id_token['sub']
    if result['user_id'] != g_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_g_id = login_session.get('g_id')
    if stored_access_token is not None and g_id == stored_g_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['g_id'] = g_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #user_id = login_session['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['g_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)