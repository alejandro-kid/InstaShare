import connexion
import json
import os
import pytest

from config import instashare
from db_config import db
from models.user_model import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", "instashare_test")
DB_HOST = os.getenv("DB_HOST", "localhost")

instashare_test = connexion.FlaskApp(__name__)
instashare_test.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME_TEST}"
)
instashare_test.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
instashare_test.app.config["SECRET_KEY"] = "mysecret"
db.init_app(instashare_test.app)
instashare_test.add_api('../swagger/swagger.yml')


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(instashare_test.app.config["SQLALCHEMY_DATABASE_URI"])
    db.Model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    db.Model.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def client():
    with instashare_test.app.test_client() as c:
        yield c


def fill_drones(db_session):
    user = User("roberto@gmail.com", "123qwe")
    db_session.add(user)
    db_session.commit()


def test_register_user(client):

    td_email = "fabian@gmail.com"
    td_password = "123qwe"

    response = client.post('/auth/register', data=json.dumps(dict(
        email=td_email,
        password=td_password
    )), mimetype='application/json')

    assert response.status_code == 201
    assert response.content_type == 'application/json'


def test_registered_with_already_registered_user(client):
    
    td_email = "roberto@gmail.com"
    td_password = "123qwe"
    response = client.post('/auth/register', data=json.dumps(dict(
    email=td_email,
    password=td_password
    )), mimetype='application/json')

    assert response.status_code == 202
    assert response.content_type == 'application/json'


def test_non_registered_user_login(self):

    td_email = "fabian@gmail.com"
    td_password = "123qwe"

    response = client.post('/auth/login', data=json.dumps(dict(
        email=td_email,
        password=td_password
    )), mimetype='application/json')

    assert response.status_code == 404
    assert response.content_type == 'application/json'
