from flask import Blueprint, request, jsonify, abort
from . import schemas, services

from flask_pydantic import validate

bond_bp = Blueprint('bond_routes', __name__, url_prefix='/api/v1/bonds')

@bond_bp.route("/", methods=['GET'])
def get_bond():
    if request.args.get('legal_name'):
        return jsonify(f"Legal name provided {request.args.get('legal_name')}")
    return "Bonds Get Route"

@bond_bp.route("", methods=["POST"])
def create_bond():
    return ItemService.get_all()


user_bp = Blueprint('user_routes', __name__, url_prefix='/api/v1/users')

@user_bp.route("", methods=['GET'])
def get_users():
    return jsonify(services.get_users()), 200


@user_bp.route("", methods=['POST'])
@validate(body=schemas.UserCreate)
def create_user(body: schemas.UserCreate):
    from email_validator import validate_email, EmailNotValidError
    try:
        valid = validate_email(body.email)
        body.email = valid.email
        user = services.create_user(body)
        access_token = services.security.create_access_token(data={"sub": "user_id:"+str(user['id'])})
        return jsonify({"data": {"user": user, "access_token": access_token}, "msg": "Successfully created new user"}), 201

    except EmailNotValidError as e:
        abort(400, e)

