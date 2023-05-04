from flask import Response
from db_config import db


def create_db():
    db.drop_all()
    db.create_all()
    response_text = '{ "message": "Database created." }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def welcome():
    response_text = '{ "message": "Hello, welcome to sdetAutomation flask-api" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def health():
    response_text = '{ "status": "OK" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response
