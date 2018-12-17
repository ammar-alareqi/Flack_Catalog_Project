from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    #categories = session.query(Category).all()
    #items = session.query(Item).all()
    return render_template('catalog.html')


@app.route('/catalog/category/')
def showCategory():
    # add your code
    # return render_template('categories.html')
    pass


@app.route('/catalog/item/')
def showItem():
    # add your code
    return render_template('items.html')


@app.route('/catalog/category/user/')
def showCategoryUser():
    # add your code
    # return render_template('categories_user.html')
    pass


@app.route('/catalog/item/user/')
def showItemUser():
    # add your code
    return render_template('items_user.html')


@app.route('/catalog/add/')
def addItem():
    # enter crud code
    return render_template('add.html')


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
    return render_template('login.html')


@app.route('/catalog/logout/')
def logout():
    return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)