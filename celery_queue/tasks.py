import base64
import gzip
import os
from celery import Celery
from google.cloud import storage


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
service_account_info = {
    "type": "service_account",
    "project_id": os.getenv("PROYECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token"
}
BUCKET = os.getenv("BUCKET", "insta-share-store")

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
storage_client = storage.Client.from_service_account_info(service_account_info)


@celery.task(name='tasks.upload_file')
def upload_file(file:str, path:str) -> None:

    # Decodifica el objeto en string codificado.
    decoded_string = base64.b64decode(file)
    #Compress data
    compressed_data = gzip.compress(decoded_string)
    path_without_extension = os.path.splitext(path)[0]
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(path_without_extension + ".zip")
    blob.upload_from_string(compressed_data)
