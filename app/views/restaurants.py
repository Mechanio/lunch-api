from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import RestaurantModel
from app.decorators import admin_group_required


restaurants_bp = Blueprint('restaurants', __name__)


@restaurants_bp.route("/api/restaurants/", methods=["GET"])
def get_restaurants():
    """
    Get all restaurants
    :return: json with restaurants info
    """
    restaurants = RestaurantModel.return_all(0, 500)

    return jsonify(restaurants)


@restaurants_bp.route("/api/restaurants/<int:id_>", methods=["GET"])
def get_restaurant(id_):
    """
    Get restaurant info by id
    :param id_: id of restaurant
    :return: json with restaurant info
    """
    restaurant = RestaurantModel.find_by_id(id_)
    if not restaurant:
        return jsonify({"message": "Restaurant not found."}), 404

    return jsonify(restaurant)


@restaurants_bp.route("/api/restaurants/", methods=["POST"])
@jwt_required()
@admin_group_required
def create_restaurant():
    """
    Create restaurant
    :return: json with new restaurant id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "name".'}), 400

    name = request.json.get("name")

    if not name:
        return jsonify({"message": 'Please, specify "name".'}), 400
    restaurant = RestaurantModel(name=name)
    restaurant.save_to_db()

    return jsonify({"id": restaurant.id}), 201


@restaurants_bp.route("/api/restaurants/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_restaurant(id_):
    """
    Update restaurant info by id
    :param id_: id of restaurant
    :return: json with message "Updated"
    """
    name = request.json.get("name")

    restaurant = RestaurantModel.find_by_id(id_, to_dict=False)
    if not restaurant:
        return jsonify({"message": "Restaurant not found."}), 404

    if name:
        restaurant.name = name
    restaurant.save_to_db()

    return jsonify({"message": "Updated"})


@restaurants_bp.route("/api/restaurants/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_restaurant(id_):
    """
    Delete restaurant by id
    :param id_: id of restaurant
    :return: json with message "Deleted"
    """
    restaurant = RestaurantModel.delete_by_id(id_)
    if restaurant == 404:
        return jsonify({"message": "Restaurant not found."}), 404
    return jsonify({"message": "Deleted"})