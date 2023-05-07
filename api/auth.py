from flask import Response, request, json
from models.user_model import User
from db_config import db


def register_user():
    request_data = request.get_json()
    user = User.query.filter_by(email=request_data["email"]).first()
    if not user:
        try:
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
        except Exception as e:
            response = Response(e, status=400, mimetype="application/json")
    else:
        data = {
            "success": False,
            "message": "User already exists. Please Log in."
        }
        response = Response(json.dumps(data), status=409, \
            mimetype="application/json")
    return response
