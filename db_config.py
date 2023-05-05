from config import instashare
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy(instashare.app)
bcrypt =  Bcrypt(instashare.app)
