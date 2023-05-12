import connexion
import os

instashare = connexion.App(__name__, specification_dir='./swagger')

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "instashare")
DB_HOST = os.getenv("DB_HOST", "localhost")

service_account_info = {
    "type": "service_account",
    "project_id": os.getenv("PROYECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
}

# configuration
instashare.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME}"
)
instashare.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
instashare.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "neO1Bhfajt")
instashare.app.config["BUCKET"] = os.getenv("BUCKET", "insta-share-store")
instashare.app.config["SERVICE_ACCOUNT_INFO"] = service_account_info

instashare.add_api('swagger.yml')
