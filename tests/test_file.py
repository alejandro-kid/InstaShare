import base64
import json
import os

from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import from_regex
from tests.conftest import helper, uuid_regex
from google.cloud import storage
from celery_queue.tasks import upload_file
from models.user_model import User


def test_upload_file_model(client, app):

    with app.app_context():
        registered_client = User.query.filter_by(email="olgacorina@gmail.com").first()

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=registered_client.id,
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{registered_client.id}/blue.zip'
    assert file_info["data"]["user"] == registered_client.id
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True

    upload_file(decoded_string, f'{registered_client.id}/blue.zip')

    # Autenticarse con las credenciales de tu cuenta de servicio
    client = \
        storage.Client.from_service_account_info(app.config["SERVICE_ACCOUNT_INFO"])

    # Obtener una referencia al archivo que deseas verificar
    bucket = client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


def test_upload_existed_file_model(client, app):

    with app.app_context():
        registered_client = User.query.filter_by(email="olgacorina@gmail.com").first()

    image_path = os.path.join(app.root_path, "files/blue.jpg")

    with open(image_path, 'rb') as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        decoded_string = encoded_content.decode("utf-8") 


    file_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=registered_client.id,
        file_name="blue.jpg",
        file=decoded_string
    )), mimetype='application/json')

    file_info = helper(file_response.response)

    assert file_response.status_code == 201
    assert file_response.content_type == 'application/json'
    assert file_info["data"]["file"]["name"] == "blue.jpg"
    assert file_info["data"]["file"]["path"] == \
        f'{registered_client.id}/blue.zip'
    assert file_info["data"]["user"] == registered_client.id
    assert file_info["message"] == "File uploaded successfully"
    assert file_info["success"] is True

    upload_file(decoded_string, f'{registered_client.id}/blue.zip')

    # Autenticarse con las credenciales de tu cuenta de servicio
    google_client = \
        storage.Client.from_service_account_info(app.config["SERVICE_ACCOUNT_INFO"])

    # Obtener una referencia al archivo que deseas verificar
    bucket = google_client.get_bucket(app.config["BUCKET"])
    blob = bucket.blob(file_info["data"]["file"]["path"])

    assert blob.exists() is True


    file_two_response = client.post('/upload_file', data=json.dumps(dict(
        user_id=registered_client.id,
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
