from datetime import datetime, timedelta
from jose import JWTError, jwt
from hashlib import sha256
import secrets
from fastapi import HTTPException, status
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Simple password hashing without bcrypt dependencies
def verify_password(plain_password, hashed_password):
    # For development - use proper hashing in production
    return get_password_hash(plain_password) == hashed_password

def get_password_hash(password):
    # Simple SHA-256 hash with salt for development
    # In production, consider using argon2 or bcrypt with proper installation
    salt = "boarding_house_salt_2024"  # In production, use a random salt per user
    return sha256((password + salt).encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )