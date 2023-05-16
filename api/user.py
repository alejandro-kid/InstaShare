import json

from flask import Response
from models.file_model import File
from models.user_model import User


def get_user_information(user):
    try:
        user = User.query.filter_by(id=user).first()

        if user:
            files = File.query.filter_by(user_owner=user.id).all()
            data = {
                "success": True,
                "message": "User information retrieved successfully",
                "data": {
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "files": [
                            {
                                "name": file.name,
                                "path": user.id + "/" + file.name
                            } for file in files
                        ]
                    }
                }
            }
            response = Response(json.dumps(data), status=200, \
                                mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "User not found"
            }
            response = Response(json.dumps(data), status=404, \
                                mimetype="application/json")
    except Exception as exc:
        response = Response(str(exc), 500, mimetype="application/json")
    
    return response