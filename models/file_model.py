import json
import os
import uuid

from db_config import db


class File(db.Model):
    """ File model for storing file related details """
    __tablename__ = "file"

    id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    user_owner = db.Column(db.String(100), db.ForeignKey('user.id'))
    __table_args__ = (db.UniqueConstraint('name', 'user_owner', name='_name_user_uc'),)



    def __init__(self, name, user_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.user_owner = user_id

    def __repr__(self):
        location_object = {
            "id": self.id,
            "name": self.name,
            "path": self.user_owner + "/" + \
                os.path.splitext(self.name)[0] + ".zip"
        }
        return json.dumps(location_object)

