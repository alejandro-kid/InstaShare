import connexion
import os


instashare = connexion.App(__name__, specification_dir='./swagger')

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "instashare")
DB_HOST = os.getenv("DB_HOST", "localhost")

# configuration
instashare.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME}"
)
instashare.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
instashare.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "neO1Bhfajt")
instashare.app.config["BUCKET"] = os.getenv("BUCKET", "insta-share-store")

instashare.app.config["CELERY_BROKER_URL"] = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
instashare.app.config["CELERY_RESULT_BACKEND"] = \
    os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

instashare.add_api('swagger.yml')
