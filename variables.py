import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
LAMBDA_API = os.getenv('LAMBDA_API')
LAMBDA_API_KEY = os.getenv('LAMBDA_API_KEY')
