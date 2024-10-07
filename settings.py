import os

from dotenv import load_dotenv

load_dotenv()

class Settings:

    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
    AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
