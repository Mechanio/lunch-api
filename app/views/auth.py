from flask import jsonify, request, Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, jwt_required, get_jwt_identity)
from app.models import EmployeeModel, RevokedTokenModel

auth_bp = Blueprint('auth', __name__)


def get_groups(employee):
    group_list = []
    if employee.is_admin:
        group_list.append("admin")
    if employee.is_active:
        group_list.append("customer")
    return {"groups": group_list}


@auth_bp.route("/api/auth/registration", methods=["POST"])
def register():
    """
    Method for adding a new employee (registration)
    :return: access and refresh tokens
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
    try:
        employee.save_to_db()
        groups = get_groups(employee)
        access_token = create_access_token(identity=email, additional_claims=groups)
        refresh_token = create_refresh_token(identity=email, additional_claims=groups)
        return {
            "id": employee.id,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong while creating",
            "error": repr(e),
        }, 500


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Method for logination
    :return: access and refresh tokens
    """
    if not request.json or not request.json.get("email") or not request.json.get("password"):
        return jsonify({"message": 'Please, provide "email" and "password" in body'}), 400

    email = request.json["email"]
    password = request.json["password"]
    current_employee = EmployeeModel.find_by_email(email, to_dict=False)
    if not current_employee:
        return {"message": f"User with email {email} doesn't exist"}, 404

    groups = get_groups(current_employee)
    if EmployeeModel.verify_hash(password, current_employee.hashed_password):
        access_token = create_access_token(identity=email, additional_claims=groups)
        refresh_token = create_refresh_token(identity=email, additional_claims=groups)
        return {
            "message": f"Logged in as {current_employee.firstname + ' ' + current_employee.lastname}, "
                       f"({current_employee.email})",
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, 201
    else:
        return {"message": "Wrong password"}, 404


@auth_bp.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def post():
    """
    Refreshing access token
    :return: new access token
    """
    current_employee_identity = get_jwt_identity()
    email = get_jwt().get("sub")
    current_employee = EmployeeModel.find_by_email(email, to_dict=False)
    if not current_employee:
        return {"message": f"User with email {email} doesn't exist"}, 404
    groups = get_groups(current_employee)
    access_token = create_access_token(identity=current_employee_identity, additional_claims=groups)
    return {'access_token': access_token}, 201


@auth_bp.route("/api/auth/logout-access", methods=["POST"])
@jwt_required()
def logout_access():
    """
    Revoke access token
    :return: message 'Access token has been revoked'
    """
    jti = get_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {'message': 'Access token has been revoked'}, 200
    except Exception as e:
        return {
            "message": "Something went wrong while revoking token",
            "error": repr(e),
        }, 500


@auth_bp.route("/api/auth/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    """
    Revoke refresh token
    :return: message 'Refresh token has been revoked'
    """
    jti = get_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": "Refresh token has been revoked"}, 200
    except Exception as e:
        return {
                   "message": "Something went wrong while revoking token",
                   "error": repr(e),
               }, 500
