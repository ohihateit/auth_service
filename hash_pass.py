import hashlib
import os

from users import users


class HashPass:
    def __init__(self) -> None:
        self.salt = os.environ['SALT']

    def _hash(self, password: str):
        return hashlib.sha256((password + self.salt).encode()).hexdigest().lower()

    def verify_password(self, username: str, password: str) -> bool:
        password_hash = self._hash(password)
        stored_password_hash = users[username]['password'].lower()

        return password_hash == stored_password_hash
