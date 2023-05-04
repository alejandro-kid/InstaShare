from config import instashare
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(instashare.app)
