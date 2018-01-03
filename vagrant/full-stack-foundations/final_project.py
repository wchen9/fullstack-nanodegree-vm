from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	#if restaurants == []:
	#	return "No restaurants"
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurant/<int:rid>/edit/', methods=['GET', 'POST'])
def editRestaurant(rid):
	restaurant = session.query(Restaurant).filter_by(id = rid).first()
	if restaurant == None:
		return redirect(url_for('showRestaurants'))
	if request.method == 'POST':
		restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:rid>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(rid):
	restaurant = session.query(Restaurant).filter_by(id = rid).first()
	if restaurant == None:
		return redirect(url_for('showRestaurants'))
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:rid>/')
@app.route('/restaurant/<int:rid>/menu/')
def showMenu(rid):
	restaurant = session.query(Restaurant).filter_by(id = rid).first()
	if restaurant == None:
		return redirect(url_for('showRestaurants'))
	items = session.query(MenuItem).filter_by(restaurant_id = rid).all()
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:rid>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(rid):
	restaurant = session.query(Restaurant).filter_by(id = rid).first()
	if restaurant == None:
		return redirect(url_for('showRestaurants'))
	if request.method == 'POST':
		item = MenuItem(name = request.form['name'], restaurant = restaurant)
		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', rid = rid))
	else:
		return render_template('newmenuitem.html', restaurant = restaurant)

@app.route('/restaurant/<int:rid>/menu/<int:iid>/edit/', methods=['GET', 'POST'])
def editMenuItem(rid, iid):
	item = session.query(MenuItem).filter_by(id = iid).first()
	if item == None:
		return redirect(url_for('showMenu', rid = rid))
	if request.method == 'POST':
		item.name = request.form['name']
		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', rid = rid))
	else:
		return render_template('editmenuitem.html', item = item)

@app.route('/restaurant/<int:rid>/menu/<int:iid>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(rid, iid):
	item = session.query(MenuItem).filter_by(id = iid).first()
	if item == None:
		return redirect(url_for('showMenu', rid = rid))
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showMenu', rid = rid))
	else:
		return render_template('deletemenuitem.html', item = item)

if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5050)