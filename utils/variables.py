import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
LAMBDA_API = os.getenv('LAMBDA_API')
LAMBDA_API_KEY = os.getenv('LAMBDA_API_KEY')
INVENTORY_QUEUE = os.getenv('INVENTORY_QUEUE')
PAYMENTS_QUEUE = os.getenv('PAYMENTS_QUEUE')
EMAIL_QUEUE = os.getenv('EMAIL_QUEUE')
ENV = os.getenv('ENV')
LOKI_URL = os.getenv('LOKI_URL')
