import jwt
import time

from os import environ

JWT_SECRET = environ['KEY']
JWT_ALGORITHM = "HS256"


class JWTToken:
    def token_response(self, token: str):
        return {"access_token": token}

    def sign_JWT(self, user_id):
        payload = {
            "user_id": user_id,
            "expires": time.time() + 600
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token

    def decode_JWT(self, token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}
