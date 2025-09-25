from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from .models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return {"message": "Pizza API is running"}, 200


# ------------------------
# Restaurants
# ------------------------
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{"id": r.id, "name": r.name, "address": r.address} for r in restaurants])


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "restaurant_pizzas": [
            {
                "id": rp.id,
                "price": rp.price,
                "pizza_id": rp.pizza_id,
                "restaurant_id": rp.restaurant_id,
            }
            for rp in restaurant.restaurant_pizzas
        ],
    }


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404

    db.session.delete(restaurant)
    db.session.commit()
    return "", 204


# ------------------------
# Pizzas
# ------------------------
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in pizzas])


# ------------------------
# Restaurant Pizzas
# ------------------------
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        new_rp = RestaurantPizza(
            price=data.get("price"),
            pizza_id=data.get("pizza_id"),
            restaurant_id=data.get("restaurant_id")
        )
        db.session.add(new_rp)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"errors": ["validation errors"]}, 400

    return {
        "id": new_rp.id,
        "price": new_rp.price,
        "pizza_id": new_rp.pizza_id,
        "restaurant_id": new_rp.restaurant_id,
        "pizza": {
            "id": new_rp.pizza.id,
            "name": new_rp.pizza.name,
            "ingredients": new_rp.pizza.ingredients
        },
        "restaurant": {
            "id": new_rp.restaurant.id,
            "name": new_rp.restaurant.name,
            "address": new_rp.restaurant.address
        }
    }, 201
