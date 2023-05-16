import os
import jsonschema

from celery_worker import celery
from flask import Response, request, json
from schemas.file_schema import upload_file_schema
from models.user_model import User
from models.file_model import File

def upload_file(user):
    try:
        request_data = request.get_json()
        jsonschema.validate(request_data, upload_file_schema)

        file = request_data["file"]
        file_name = request_data["file_name"]

        current_user = User.query.filter_by(id=user).first()

        if current_user:
            existed_file = \
                File.query.filter_by(user_owner=user, name=file_name).first()
            if  not existed_file:

                celery.send_task('tasks.upload_file', args=[file, \
                        "{}/{}".format(user, file_name)])

                file = current_user.add_file(file_name)

                data = {
                    "success": True,
                    "message": "File uploaded successfully",
                    "data": {
                        "user": user,
                        "file": {
                            "name": file.name,
                            "path": user + "/" + os.path.splitext(file.name)[0] \
                                + ".zip"
                        }
                    }
                }
                response = Response(json.dumps(data), status=201, \
                                    mimetype="application/json")
            else:
                data = {
                    "success": False,
                    "message": "File already exists"
                }
                response = Response(json.dumps(data), status=409, \
                                    mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "User not found"
            }
            response = Response(json.dumps(data), status=404, \
                                mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")

    return response

