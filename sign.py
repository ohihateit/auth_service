import base64
import hmac
import hashlib
from typing import Optional


class Sign:
    def __init__(self, key):
        self.KEY = key

    def sign_data(self, data: str) -> str:
        return hmac.new(self.KEY.encode(), msg=data.encode(), digestmod=hashlib.sha256).hexdigest().upper()

    def get_username_from_signed_cookie(self, username_signed: str) -> Optional[str]:
        try:
            username_base64, sign = username_signed.split('.')
            username = base64.b64decode(username_base64.encode()).decode()
        except AttributeError:
            return None

        valid_sign = self.sign_data(data=username)

        if hmac.compare_digest(valid_sign, sign):
            return username
