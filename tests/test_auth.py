import json
import re
from tests.conftest import helper, uuid_regex


def test_welcome(client):
    response = client.get("/")
    assert response.status_code == 200



def test_register_user(client):

    td_name = "Fabian Piñeiro"
    td_email = "fabian@gmail.com"
    td_password = "CIDEmiNebtL"

    response = client.post('/user/register', data=json.dumps(dict(
        name=td_name,
        email=td_email,
        password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert json_info["data"]["name"] == td_name
    assert json_info["data"]["email"] == td_email
    assert re.match(uuid_regex, json_info["data"]["id"])



def test_registered_with_already_registered_user(client):

    td_name = "Roberto Palomares"
    td_email = "roberto@gmail.com"
    td_password = "CIDEmiNebtL"
    response = client.post('/user/register', data=json.dumps(dict(
    name=td_name,
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 409
    assert response.content_type == 'application/json'
    assert json_info["message"] == "User already exists. Please Log in."
    assert json_info["success"] is False


def test_user_login(client):

    td_email = "roberto@gmail.com"
    td_password = "CIDEmiNebtL"
    response = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    jwt_regex = r"^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$"

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["message"] == "Logged successfully"
    assert re.match(jwt_regex, json_info["token"])
    assert json_info["success"] is True


def test_user_login_fail(client):

    td_email = "fabian@gmail.com"
    td_password = "CIDEmiNebtL"
    response = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["message"] == "Logged fail"
    assert json_info["success"] is False


def test_correct_autorization(client):

    td_email = "roberto@gmail.com"
    td_password = "CIDEmiNebtL"
    response = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    response_client = client.get('/user', headers={"Authorization": "Bearer " + \
                                                   json_info["token"]})

    json_info_client = helper(response_client.response)

    assert response_client.status_code == 200
    assert response_client.content_type == 'application/json'
    assert json_info_client["success"] is True
    assert json_info_client["message"] == "User information retrieved successfully"
    assert json_info_client["data"]["user"]["name"] == "Roberto Palomares"
    assert json_info_client["data"]["user"]["email"] == "roberto@gmail.com"
