from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app.models import EmployeeModel
from app.decorators import admin_group_required

employees_bp = Blueprint('employees', __name__)


@employees_bp.route("/api/employees/", methods=["GET"])
@jwt_required()
def get_employees():
    """
    Get all employees or by name
    :return: json with employees info
    """
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    if firstname and lastname:
        employee = EmployeeModel.find_by_name(firstname, lastname)
    elif email:
        employee = EmployeeModel.find_by_email(email)
    else:
        employee = EmployeeModel.return_all(0, 500)
    return jsonify(employee)


@employees_bp.route("/api/employees/inactive", methods=["GET"])
@jwt_required()
@admin_group_required
def get_inactive_employees():
    """
    Get all inactive employees
    :return: json with employees info
    """
    employee = EmployeeModel.return_all_inactive(0, 500)
    return jsonify(employee)


@employees_bp.route("/api/employees/current", methods=["GET"])
@jwt_required()
def get_current_employee():
    """
    Get current employee info by jwt email
    :return: json with user info
    """
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email)
    return jsonify(current_employee)


@employees_bp.route("/api/employees/<int:id_>", methods=["GET"])
@jwt_required()
def get_employee(id_):
    """
    Get user info by id
    :param id_: id of employee
    :return: json with employee info
    """
    employee = EmployeeModel.find_by_id(id_)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404

    return jsonify(employee)


@employees_bp.route("/api/employees/", methods=["POST"])
@jwt_required()
@admin_group_required
def create_employee():
    """
    Create employee as admin
    :return: json with new employee id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "firstname", "lastname", "email", "password" and "is_admin".'}), 400

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    email = request.json.get("email")
    password = request.json.get("password")
    is_admin = request.json.get("is_admin")

    if not firstname or not lastname or not email or not password or not isinstance(is_admin, bool):
        return jsonify({"message": 'Please, specify "firstname", "lastname", "email", "password" and "is_admin".'}), 400

    if EmployeeModel.find_by_email(email, to_dict=False):
        return {"message": f"Email {email} already used"}, 404

    employee = EmployeeModel(firstname=firstname, lastname=lastname, email=email,
                             hashed_password=EmployeeModel.generate_hash(password), is_admin=is_admin, is_active=True)
    employee.save_to_db()
    return jsonify({"id": employee.id}), 201


@employees_bp.route("/api/employees/<int:id_>", methods=["PATCH"])
@jwt_required()
def update_employee(id_):
    """
    Update employee info by id as admin or only password as employee
    :param id_: id of employee
    :return: json with message "Updated"
    """
    employee = EmployeeModel.find_by_id(id_, to_dict=False)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    errors = {}
    if "admin" in groups:
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        password = request.json.get("password")
        is_admin = request.json.get("is_admin")
        is_active = request.json.get("is_active")

        if firstname:
            employee.firstname = firstname
        if lastname:
            employee.lastname = lastname
        if email:
            if not EmployeeModel.find_by_email(email, to_dict=False):
                employee.email = email
            else:
                errors = {"message": f"Updated, but email {email} already used"}

        if isinstance(is_admin, bool):
            employee.is_admin = is_admin
        if isinstance(is_active, bool):
            employee.is_active = is_active
        if password:
            employee.hashed_password = EmployeeModel.generate_hash(password)
        employee.save_to_db()
    else:
        password = request.json.get("password")
        if current_employee.id == employee.id:
            if password:
                employee.hashed_password = EmployeeModel.generate_hash(password)
            employee.save_to_db()
        else:
            return jsonify({"message": "Not allowed"}), 404
    if errors:
        return jsonify(errors)
    else:
        return jsonify({"message": "Updated"})


@employees_bp.route("/api/employees/<int:id_>", methods=["DELETE"])
@jwt_required()
def delete_employee(id_):
    """
    Delete employee by id
    :param id_: id of employee
    :return: json with message "Deleted"
    """
    employee = EmployeeModel.find_by_id(id_)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    if "admin" not in groups:
        if current_employee.id != employee["id"]:
            return jsonify({"message": "Not allowed"}), 405
    employee = EmployeeModel.delete_by_id(id_)
    return jsonify({"message": "Deleted"})
