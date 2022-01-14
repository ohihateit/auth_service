import jwt
import time

from os import environ

JWT_SECRET = environ['KEY']
JWT_ALGORITHM = "HS256"


class JWTToken:
    @staticmethod
    def sign_JWT(user_id):
        payload = {
            "user_id": user_id,
            "expires": time.time() + 600
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token

    @staticmethod
    def decode_JWT(token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}
