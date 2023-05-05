import datetime
import json
import uuid


from db_config import db, bcrypt
from config import instashare


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, instashare.app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()


    def __repr__(self):
        location_object = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'registered_on': self.registered_on,
        }
        return json.dumps(location_object)

