import json
import jsonschema

from db_config import db
from flask import Response, request
from models.user_model import User
from schemas.user_schema import register_user_schema, login_user_schema

def register_user():
    try:
        request_data = request.get_json()
        jsonschema.validate(request_data, register_user_schema)

        user = User.query.filter_by(email=request_data["email"]).first()
        if not user:
                user = User(\
                    request_data["name"],request_data["email"], request_data["password"]
                )
                db.session.add(user)
                db.session.commit()
                data = {
                    "success": True,
                    "message": "User registered successfully",
                    "data": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email
                    }
                }
                response = Response(json.dumps(data), status=201, \
                    mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "User already exists. Please Log in."
            }
            response = Response(json.dumps(data), status=409, \
                mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response


def login():
    try:
        request_data = request.get_json()
        jsonschema.validate(request_data, login_user_schema)

        user = User.query.filter_by(email=request_data["email"]).first()
        if user:
            if user.check_password(request_data["password"]):
                data = {
                    "success": True,
                    "message": "Logged successfully",
                    "data": {
                        "id": user.id
                    }
                }
                response = Response(json.dumps(data), status=202, \
                    mimetype="application/json")
            else:
                data = {
                    "success": False,
                    "message": "Logged fail"
                }
                response = Response(json.dumps(data), status=202, \
                    mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "Logged fail"
            }
            response = Response(json.dumps(data), status=202, \
                mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")

    return response