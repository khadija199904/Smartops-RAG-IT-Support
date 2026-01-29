from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()


PDF_PATH = os.getenv("DATA_PATH")

EMBEDDING_MODEL_NAME= os.getenv("EMBEDDING_MODEL_NAME")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR")

# 2 eme methode 
HF_TOKEN = os.getenv("HF_TOKEN")


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL :
    # Fetch variables
     USER = os.getenv("user")
     PASSWORD = os.getenv("password")
     HOST = os.getenv("host")
     PORT = os.getenv("port")
     DBNAME = os.getenv("dbname")


     # Construct the SQLAlchemy connection string
     DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")