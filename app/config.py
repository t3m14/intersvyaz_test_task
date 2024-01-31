from dotenv import load_dotenv
import os 

load_dotenv()

SQLALCHEMY_DATABSE_URI = os.environ.get("SQLALCHEMY_DATABSE_URI")