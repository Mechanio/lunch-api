from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import MenusModel, RestaurantModel
from app.decorators import admin_group_required

menus_bp = Blueprint('menus', __name__)


@menus_bp.route("/api/menus/", methods=["GET"])
def get_menus():
    """
    Get all menus
    :return: json with menus info
    """
    menus = MenusModel.return_all(0, 500)

    return jsonify(menus)


@menus_bp.route("/api/menus/<int:id_>", methods=["GET"])
def get_menu(id_):
    """
    Get menu info by id
    :param id_: id of menu
    :return: json with menu info
    """
    menu = MenusModel.find_by_id(id_)
    if not menu:
        return jsonify({"message": "Menu not found."}), 404

    return jsonify(menu)


@menus_bp.route("/api/menus/", methods=["POST"])
@jwt_required()
@admin_group_required
def create_menu():
    """
    Create menu
    :return: json with new menu id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "restaurant_id", '
                                   '"monday", "tuesday", "wednesday", "thursday",'
                                   ' "friday", "saturday", "sunday".'}), 400

    restaurant_id = request.json.get("restaurant_id")
    monday = request.json.get("monday")
    tuesday = request.json.get("tuesday")
    wednesday = request.json.get("wednesday")
    thursday = request.json.get("thursday")
    friday = request.json.get("friday")
    saturday = request.json.get("saturday")
    sunday = request.json.get("sunday")

    if RestaurantModel.find_by_id(restaurant_id, to_dict=False) == {}:
        return {"message": f"Restaurant not found. "}, 404
    if MenusModel.find_by_restaurant_id(restaurant_id, to_dict=False):
        return {"message": f"This restaurant already has a menu. "}, 404

    if not restaurant_id or not monday or not tuesday or not wednesday or not thursday \
            or not friday or not saturday or not sunday:
        return jsonify({"message": 'Please, specify restaurant_id, monday, '
                                   'tuesday, wednesday, thursday, friday, saturday, sunday.'}), 400
    menu = MenusModel(restaurant_id=restaurant_id, monday=monday,
                      tuesday=tuesday, wednesday=wednesday, thursday=thursday,
                      friday=friday, saturday=saturday, sunday=sunday)
    menu.save_to_db()

    return jsonify({"id": menu.id}), 201


@menus_bp.route("/api/menus/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_menu(id_):
    """
    Update menu info by id
    :param id_: id of menu
    :return: json with message "Updated"
    """
    restaurant_id = request.json.get("restaurant_id")
    monday = request.json.get("monday")
    tuesday = request.json.get("tuesday")
    wednesday = request.json.get("wednesday")
    thursday = request.json.get("thursday")
    friday = request.json.get("friday")
    saturday = request.json.get("saturday")
    sunday = request.json.get("sunday")

    menu = MenusModel.find_by_id(id_, to_dict=False)
    if not menu:
        return jsonify({"message": "Menu not found."}), 404

    if restaurant_id:
        if RestaurantModel.find_by_id(restaurant_id, to_dict=False) == {}:
            return {"message": f"Restaurant not found. "}, 404
        if MenusModel.find_by_restaurant_id(restaurant_id, to_dict=False):
            return {"message": f"This restaurant already has a menu. "}, 404
        menu.restaurant_id = restaurant_id
    if monday:
        menu.monday = monday
    if tuesday:
        menu.tuesday = tuesday
    if wednesday:
        menu.wednesday = wednesday
    if thursday:
        menu.thursday = thursday
    if friday:
        menu.friday = friday
    if saturday:
        menu.saturday = saturday
    if sunday:
        menu.sunday = sunday

    menu.save_to_db()

    return jsonify({"message": "Updated"})


@menus_bp.route("/api/menus/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_menu(id_):
    """
    Delete menu by id
    :param id_: id of menu
    :return: json with message "Deleted"
    """
    menu = MenusModel.delete_by_id(id_)
    if menu == 404:
        return jsonify({"message": "Menu not found."}), 404
    return jsonify({"message": "Deleted"})
