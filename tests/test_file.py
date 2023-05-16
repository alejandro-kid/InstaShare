import base64
import json
import os

from tests.conftest import helper
from google.cloud import storage
from celery_queue.tasks import upload_file


def test_upload_file_model(client, app):

    td_email = "olgacorina@gmail.com"
    td_password = "123alekajsnd"
    response_login = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    login_info = helper(response_login.response)

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json', headers={"Authorization": "Bearer " + \
                                                   login_info["token"]})

    response_user = client.get('/user', headers={"Authorization": "Bearer " + \
                                                   login_info["token"]})

    user_info = helper(response_user.response)

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{user_info["data"]["user"]["id"]}/blue.zip'
    assert file_info["data"]["user"] == user_info["data"]["user"]["id"]
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True

    upload_file(decoded_string, f'{user_info["data"]["user"]["id"]}/blue.zip')

    # Autenticarse con las credenciales de tu cuenta de servicio
    client = \
        storage.Client.from_service_account_json("instashare-credentials.json")

    # Obtener una referencia al archivo que deseas verificar
    bucket = client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


def test_upload_existed_file_model(client, app):

    td_email = "olgacorina@gmail.com"
    td_password = "123alekajsnd"
    response_login = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    login_info = helper(response_login.response)

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json', headers={"Authorization": "Bearer " + \
                                                   login_info["token"]})

    response_user = client.get('/user', headers={"Authorization": "Bearer " + \
                                                   login_info["token"]})

    user_info = helper(response_user.response)

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{user_info["data"]["user"]["id"]}/blue.zip'
    assert file_info["data"]["user"] == user_info["data"]["user"]["id"]
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True

    upload_file(decoded_string, f'{user_info["data"]["user"]["id"]}/blue.zip')

    # Autenticarse con las credenciales de tu cuenta de servicio
    google_client = \
        storage.Client.from_service_account_json("instashare-credentials.json")

    # Obtener una referencia al archivo que deseas verificar
    bucket = google_client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


    file_two_response = client.post('/upload_file', data=json.dumps(dict(
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json', headers={"Authorization": "Bearer " + \
                                                   login_info["token"]})

    file_two_info = helper(file_two_response.response)

    assert file_two_response.status_code == 409
    assert file_two_response.content_type == 'application/json'
    assert file_two_info["message"] == "File already exists"
    assert file_two_info["success"] is False
