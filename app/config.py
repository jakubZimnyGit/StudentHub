from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY1")
    ALGORITHM = os.getenv("ALGORITHM1")
    TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE_MINUTES")