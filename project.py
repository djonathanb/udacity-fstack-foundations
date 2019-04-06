from flask import Flask, url_for, request, render_template, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def restaurant_menu():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash('new menu item created!')
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))

    return render_template('new_menu_item.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        item.name = request.form['name']
        session.add(item)
        session.commit()
        flash('item %s edited!' % item.name)
        return redirect(url_for('restaurant_menu'))

    return render_template('edit_menu_item.html', restaurant_id=restaurant_id, item=item)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('item %s deleted!' % item.name)
        return redirect(url_for('restaurant_menu'))

    return render_template('delete_menu_item.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
