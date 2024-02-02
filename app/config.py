from dotenv import load_dotenv
import os 

load_dotenv()

# SQLALCHEMY_DATABSE_URI = os.environ.get("SQLALCHEMY_DATABSE_URI")

SQLALCHEMY_DATABSE_URI =  "postgresql://postgres:postgres@localhost:4321/postgres"