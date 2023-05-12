import datetime
import json
import uuid

from models.file_model import File
from db_config import db, bcrypt
from config import instashare


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    files = db.relationship('File', backref='user')

    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, instashare.app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()


    def __repr__(self):
        location_object = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "registered_on": self.registered_on
        }
        return json.dumps(location_object)


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def add_file(self, name)->File:
        file = File(name, self.id)
        db.session.add(file)
        db.session.commit()
        return file
