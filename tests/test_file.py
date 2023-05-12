import base64
import json
import re
import os

from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import from_regex
from tests.conftest import helper, uuid_regex
from google.cloud import storage


def test_upload_file(client, app):

    td_name = "Olga Corina"
    td_email = "olgacorina@gmail.com"
    td_password = "123alekajsnd"

    user_response = client.post('/user/register', data=json.dumps(dict(
        name=td_name,
        email=td_email,
        password=td_password
    )), mimetype='application/json')

    user_info = helper(user_response.response)

    assert user_response.status_code == 201
    assert user_response.content_type == 'application/json'
    assert user_info["data"]["name"] == td_name
    assert user_info["data"]["email"] == td_email
    assert re.match(uuid_regex, user_info["data"]["id"])

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=user_info["data"]["id"],
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{user_info["data"]["id"]}/blue.zip'
    assert file_info["data"]["user"] == user_info["data"]["id"]
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True


    # Autenticarse con las credenciales de tu cuenta de servicio
    client = \
        storage.Client.from_service_account_info(app.config["SERVICE_ACCOUNT_INFO"])

    # Obtener una referencia al archivo que deseas verificar
    bucket = client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


def test_upload_existed_file(client, app):

    td_name = "Olga Corina"
    td_email = "olgacorina@gmail.com"
    td_password = "123alekajsnd"

    user_response = client.post('/user/register', data=json.dumps(dict(
        name=td_name,
        email=td_email,
        password=td_password
    )), mimetype='application/json')

    user_info = helper(user_response.response)

    assert user_response.status_code == 201
    assert user_response.content_type == 'application/json'
    assert user_info["data"]["name"] == td_name
    assert user_info["data"]["email"] == td_email
    assert re.match(uuid_regex, user_info["data"]["id"])

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=user_info["data"]["id"],
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{user_info["data"]["id"]}/blue.zip'
    assert file_info["data"]["user"] == user_info["data"]["id"]
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True


    # Autenticarse con las credenciales de tu cuenta de servicio
    google_client = \
        storage.Client.from_service_account_info(app.config["SERVICE_ACCOUNT_INFO"])

    # Obtener una referencia al archivo que deseas verificar
    bucket = google_client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


    file_two_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=user_info["data"]["id"],
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_two_info = helper(file_two_response.response)
    

    assert file_two_response.status_code == 409
    assert file_two_response.content_type == 'application/json'
    assert file_two_info["message"] == "File already exists"
    assert file_two_info["success"] is False


@given(uuid=from_regex(uuid_regex))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_upload_no_existed_user(client, app, uuid):

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=uuid,
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_info = helper(file_response.response)

    assert file_response.status_code == 404
    assert file_response.content_type == 'application/json'
    assert file_info["success"] is False
    assert file_info["message"] == "User not found"
