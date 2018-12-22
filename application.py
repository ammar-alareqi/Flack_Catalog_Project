from flask import Flask, render_template, request, redirect, jsonify, url_for, flash 
from sqlalchemy import create_engine, asc, desc 
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item
import datetime

from flask import session as login_session
import random
import string

app = Flask(__name__)

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
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items = items)


@app.route('/catalog/<int:item_id>/item_description/')
def showSelectedItem(item_id):
    selectedItem = session.query(Item).filter_by(id=item_id).all()
    return render_template('item_description.html', item = selectedItem)


@app.route('/catalog/category/user/')
def showCategoryUser():
    # add your code
    # return render_template('categories_user.html')
    pass


@app.route('/catalog/items/user/')
def showItemsUser():
    # add your code
    return render_template('items_user.html')


@app.route('/catalog/add/')
def addItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], 
            description=request.form['description'],
            date=datetime.datetime.now(),
            category=session.query(Category).filter_by(
                            name=request.form['category']).one(),
            user = login_session['used_id'])
        session.add(newItem)
        session.commit()
        flash('A new item was added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('add.html', categories=categories)


@app.route('/catalog/edit/')
def editItem():
    # enter crud code
    return render_template('edit.html')


@app.route('/catalog/delete/')
def deleteItem():
    # enter crud code
    return render_template('delete.html')


@app.route('/catalog/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/catalog/logout/')
def logout():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)