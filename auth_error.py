from typing import Dict

from fastapi.templating import Jinja2Templates


class AuthError:
    def __init__(self):
        self.templates = Jinja2Templates(directory="templates")

    def redirect_to_auth_form(self, context: Dict):
        response = self.templates.TemplateResponse("auth.html", context=context)
        AuthError._delete_cookie(response)
        return response

    @staticmethod
    def _delete_cookie(response):
        response.delete_cookie(key='username')
