import os
import connexion

# create an application instance

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
instashare.add_api('swagger.yml')
