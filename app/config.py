from dotenv import load_dotenv
import os 

load_dotenv()

# SQLALCHEMY_DATABSE_URI = os.environ.get("SQLALCHEMY_DATABSE_URI")
# ML_URL = os.environ.get("ML_URL")
ML_URL = "http://ml:8001/ml_model"
SQLALCHEMY_DATABSE_URI =  "postgresql://postgres:postgres@localhost:4321/postgres"