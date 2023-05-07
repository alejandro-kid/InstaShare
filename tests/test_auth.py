import json
import re


uuid_regex = (
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def helper(json_info)->any:
    for info in json_info:
        first_row = info.decode("utf-8")
        return json.loads(first_row)

def test_welcome(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_user(app, client):

    td_name = "Fabian Piñeiro"
    td_email = "fabian@gmail.com"
    td_password = "123qwe"

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
    td_password = "123qwe"
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
    td_password = "123qwe"
    response = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["message"] == "Logged successfully"
    assert re.match(uuid_regex, json_info["data"]["id"])
    assert json_info["success"] is True


def test_user_login_fail(client):

    td_email = "fabian@gmail.com"
    td_password = "123qwe"
    response = client.post('/user/login', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["message"] == "Logged fail"
    assert json_info["success"] is False
