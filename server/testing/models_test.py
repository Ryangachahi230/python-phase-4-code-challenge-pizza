import pytest
from faker import Faker
from server.app import app, db   
from server.models import Restaurant, RestaurantPizza, Pizza


class TestRestaurantPizza:
    '''Class RestaurantPizza in models.py'''

    def test_price_between_1_and_30(self):
        '''requires price between 1 and 30.'''
        with app.app_context():
            pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
            restaurant = Restaurant(name=Faker().name(), address='Main St')
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            rp1 = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=1)
            rp2 = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=30)
            db.session.add_all([rp1, rp2])
            db.session.commit()

    def test_price_too_low(self):
        '''fails when price is 0.'''
        with app.app_context():
            with pytest.raises(ValueError):
                pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add_all([pizza, restaurant])
                db.session.commit()

                rp = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=0)
                db.session.add(rp)
                db.session.commit()

    def test_price_too_high(self):
        '''fails when price is 31.'''
        with app.app_context():
            with pytest.raises(ValueError):
                pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add_all([pizza, restaurant])
                db.session.commit()

                rp = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=31)
                db.session.add(rp)
                db.session.commit()
