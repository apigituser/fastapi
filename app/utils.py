'''
    This file basically deals with cryptography
    IMPORTANT POINT:
    Plain_Text == Hashed_Plain_Text (if Plain_Text not changed)
'''

from passlib.context import CryptContext

## Creating a cryptography context to hash or verify a specific password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## Function used to hash a password
def hash(password: str):    
    return pwd_context.hash(password)

## Function verifies a plain password by comparing it to a hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)