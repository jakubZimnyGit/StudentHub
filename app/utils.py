from passlib.context import CryptContext
import random
import string

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password():
    characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(8))
    
    return password

def hash_password(password):
    return context.hash(password)

def verify_password(plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)