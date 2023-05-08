import pytest
import connexion
import os

from config import instashare  # noqa: F401
from db_config import db
from sqlalchemy import create_engine
from models.user_model import User


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


@pytest.fixture
def app():
    app = instashare_test.app
    engine = create_engine(instashare_test.app.config["SQLALCHEMY_DATABASE_URI"])
    db.Model.metadata.create_all(engine)

    #Data test
    td_name = "Roberto Palomares"
    td_email = "roberto@gmail.com"
    td_password = "123qwe"
    with app.app_context():
        user = User(td_name, td_email, td_password)
        db.session.add(user)
        db.session.commit()

    yield app
    db.Model.metadata.drop_all(engine)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
