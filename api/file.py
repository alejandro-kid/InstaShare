import base64
import os
import gzip

from flask import Response, request, json
from models.user_model import User
from models.file_model import File
from db_config import instashare
from google.cloud import storage
from google.oauth2 import service_account

def upload_file():
    try:
        request_data = request.get_json()

        file = request_data["file"]
        file_name = request_data["file_name"]
        user_id = request_data["user_id"]
        file_name_without_extension = os.path.splitext(file_name)[0]

        user = User.query.filter_by(id=user_id).first()

        if user:
            existed_file = File.query.filter_by(user_owner=user_id, name=file_name).first()
            if  not existed_file:

                credentials_info = \
                    instashare.app.config["SERVICE_ACCOUNT_INFO"]

                credentials = \
                    service_account.Credentials.from_service_account_info(credentials_info)
                storage_client = storage.Client(credentials=credentials)

                # Decodifica el objeto en string codificado.
                decoded_string = base64.b64decode(file)
                #Compress data
                compressed_data = gzip.compress(decoded_string)

                bucket = storage_client.bucket(instashare.app.config["BUCKET"])
                blob = bucket.blob("{}/{}".format(user_id, \
                    f"{file_name_without_extension}" + ".zip"))
                blob.upload_from_string(compressed_data)

                file = user.add_file(file_name)

                data = {
                    "success": True,
                    "message": "File uploaded successfully",
                    "data": {
                        "user": user.id,
                        "file": {
                            "name": file.name,
                            "path": user.id + "/" + os.path.splitext(file.name)[0] \
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

    except Exception as e:
        return Response(json.dumps({"message": e}), status=500, \
                        mimetype="application/json")
    return response

