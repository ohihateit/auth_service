from typing import Optional
from datetime import datetime, time, timedelta
from jose import JWTError, jwt
from os import access, environ
from pydantic import BaseModel

from main import token


class JWTToken:
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, environ['SALT'], algorith="HS256")

        return encoded_jwt


class Token(BaseModel):
    access_token: str
    token_type: str