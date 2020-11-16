from flask import Blueprint, request, jsonify, abort
from . import schemas, services
from email_validator import validate_email, EmailNotValidError
from flask_pydantic import validate
from .util import serialize_data, has_auth_header
from jose import JWTError
from functools import wraps
from .security import decode_token


token_bp = Blueprint('token_routes', __name__, url_prefix='/api/v1/token')
bond_bp = Blueprint('bond_routes', __name__, url_prefix='/api/v1/bonds')
user_bp = Blueprint('user_routes', __name__, url_prefix='/api/v1/users')


# A decorator which will check if there exists a current user from an auth token and adds to args
def get_current_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        def credentials_exception():
            abort(401, "Could not validate credentials")
        try:
            payload = decode_token(request.headers['Authorization'])
            user_id: str = payload.get("sub").split("user_id:")[1]
            if user_id is None:
                credentials_exception()

            token_data = schemas.TokenData(user_id=user_id)
        except JWTError:
            credentials_exception()
        user = services.get_user(user_id)
        if user is None:
            credentials_exception()
        # return user
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    return decorated_function


# A decorator to check the authorization header exists in a request
def has_auth_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers or 'Authorization' not in request.headers or not request.headers['Authorization']:
            abort(401, "Not authorized, please send a valid auth token")
        return f(*args, **kwargs)
    return decorated_function


@token_bp.route("", methods=['POST'])
@validate(body=schemas.UserCreate)
def get_token(body: schemas.UserCreate):
    print(body)
    user = services.authenticate_user(body.email, body.password)
    if not user:
        abort(401, "Could not validate credentials")
    access_token = services.security.create_access_token(
        data={"sub": "user_id:"+str(user.id)})
    return access_token, 200


@bond_bp.route("/", methods=['GET'])
@has_auth_header
@get_current_user
def get_bond(current_user: schemas.User):
    bonds = serialize_data(current_user.bonds, schemas.Bond)
    print(current_user.bonds)
    print(bonds)
    return jsonify(bonds), 200
    if request.args.get('legal_name'):
        return jsonify(f"Legal name provided {request.args.get('legal_name')}")
    return "Bonds Get Route"


@bond_bp.route("", methods=["POST"])
@validate(body=schemas.BondCreate)
@has_auth_header
@get_current_user
def create_bond(body: schemas.BondCreate, current_user: schemas.User):
    access_token = request.headers['Authorization']
    new_bond = services.create_bond(body, current_user.id)
    serialized_bond = serialize_data(new_bond, schemas.Bond)
    return jsonify(serialized_bond), 200


@user_bp.route("", methods=['GET'])
def get_users():
    serialized_user = serialize_data(services.get_users(), schemas.User)
    return jsonify(serialized_user), 200


@user_bp.route("", methods=['POST'])
@validate(body=schemas.UserCreate)
def create_user(body: schemas.UserCreate):
    user = services.get_user_by_email(body.email)
    if user:
        abort(400, "User with email already exists")
    try:

        valid = validate_email(body.email)
        # set body email to be normalized email
        body.email = valid.email

        new_user = services.create_user(body)
        access_token = services.security.create_access_token(
            data={"sub": "user_id:"+str(new_user.id)})

        serialized_new_user = serialize_data(new_user, schemas.User)
        return jsonify({"data": {"user": serialized_new_user, "access_token": access_token},
                        "msg": "Successfully created new user"}), 201

    except EmailNotValidError as e:
        abort(400, e)
