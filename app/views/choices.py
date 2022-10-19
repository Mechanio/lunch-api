from datetime import date

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app.models import ChoicesModel, EmployeeModel

choices_bp = Blueprint('choices', __name__)


@choices_bp.route("/api/choices/<int:id_>", methods=["GET"])
def get_choice(id_):
    """
    Get one choice info by id
    :param id_: id of choice
    :return: json with choice info
    """
    choice = ChoicesModel.find_by_id(id_)
    if not choice:
        return jsonify({"message": "Choice not found."}), 404

    return jsonify(choice)


@choices_bp.route("/api/choices/current", methods=["GET"])
def get_current_day_choices():
    """
    Get current day choices
    :return: json with choices info
    """
    choices = ChoicesModel.find_by_current_day(0, 500)
    if not choices:
        return jsonify({"message": "Choices not found."}), 404

    return jsonify(choices)


@choices_bp.route("/api/choices/", methods=["POST"])
@jwt_required()
def create_choice():
    """
    Create choice
    :return: json with new choice id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "menu_id".'}), 400
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email)

    menu_id = request.json.get("menu_id")

    if not menu_id:
        return jsonify({"message": 'Please, specify menu_id.'}), 400

    if ChoicesModel.find_by_employee_id(current_employee['id'], to_dict=False):
        return jsonify({"message": 'You have already choosen'}), 400
    choice = ChoicesModel(current_day=date.today().strftime("%Y-%m-%d"),
                          employee_id=current_employee['id'], menu_id=menu_id)
    choice.save_to_db()

    return jsonify({"id": choice.id}), 201


@choices_bp.route("/api/choices/<int:id_>", methods=["PATCH"])
@jwt_required()
def update_choice(id_):
    """
    Update choice info by id
    :param id_: id of choice
    :return: json with message "Updated"
    """
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email)

    choice = ChoicesModel.find_by_id(id_, to_dict=False)
    if not choice:
        return jsonify({"message": "Choice not found."}), 404

    if choice.employee_id != current_employee['id']:
        return jsonify({"message": "Something went wrong."}), 404

    menu_id = request.json.get("menu_id")

    if menu_id:
        choice.menu_id = menu_id
        choice.current_day = date.today().strftime("%Y-%m-%d")

    choice.save_to_db()

    return jsonify({"message": "Updated"})


@choices_bp.route("/api/choices/<int:id_>", methods=["DELETE"])
@jwt_required()
def delete_choice(id_):
    """
    Delete choice by id
    :param id_: id of choice
    :return: json with message "Deleted"
    """
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email)

    choice = ChoicesModel.find_by_id(id_, to_dict=False)
    if not choice:
        return jsonify({"message": "Choice not found."}), 404

    if choice.employee_id != current_employee['id']:
        return jsonify({"message": "Something went wrong."}), 404

    choice = ChoicesModel.delete_by_id(id_)
    if choice == 404:
        return jsonify({"message": "Choice not found."}), 404
    return jsonify({"message": "Deleted"})
