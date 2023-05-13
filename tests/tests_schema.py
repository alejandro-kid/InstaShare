import base64
import jsonschema

from hypothesis import given
from hypothesis.strategies import text, from_regex, emails
from schemas.user_schema import register_user_schema, login_user_schema
from schemas.file_schema import upload_file_schema




@given(name=text(min_size=8), email=emails(), password=text(min_size=8))
def test_schema_register_user_schema(name, email, password):

    td_post_body = {
        "name": name,
        "email": email,
        "password": password
    }
    jsonschema.validate(td_post_body, register_user_schema)


@given(email=emails(), password=text(min_size=8))
def test_schema_login_user_schema(name, email, password):

    td_post_body = {
        "name": name,
        "password": password
    }
    jsonschema.validate(td_post_body, login_user_schema)


@given(file=text(min_size=1), \
       file_name=from_regex(r'[A-Za-z0-9]{1,}\.[A-Za-z0-9]{1,4}'),
       user_id=from_regex(r'^[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}$')
    )
def test_schema_upload_file_schema(file, file_name, user_id):
    td_post_body = {
        "file": str(base64.b64encode(file.encode())),
        "file_name": file_name,
        "user_id": user_id
    }
    
    jsonschema.validate(td_post_body, upload_file_schema)
