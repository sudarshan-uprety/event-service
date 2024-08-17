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
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
REGISTER_EMAIL = 'REGISTER_EMAIL'
FORGET_PASSWORD_EMAIL = 'FORGET_PASSWORD_EMAIL'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
