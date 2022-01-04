import base64
import os
from typing import Optional
from jwt_token import Token
from fastapi import Cookie, FastAPI, Form, Request, Response
from fastapi.templating import Jinja2Templates
from auth_error import AuthError
from hash_pass import HashPass
from sign import Sign
from users import users

KEY = os.environ['KEY']

app = FastAPI()
templates = Jinja2Templates(directory="templates")
sign = Sign(key=KEY)
auth = AuthError()


@app.get("/")
async def index(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:
        return auth.redirect_to_auth_form(context={"request": request})

    valid_username = sign.get_username_from_signed_cookie(username)

    if not valid_username:
        return auth.redirect_to_auth_form(context={"request": request})

    try:
        user = users[valid_username]
    except KeyError:
        return auth.redirect_to_auth_form(context={"request": request})

    return Response(f"Hello, {users[valid_username]['name']}")


@app.post("/login")
async def login(login: str = Form(...), password: str = Form(...)):
    user = users.get(login)
    hash_pass = HashPass()

    if not user or not hash_pass.verify_password(login, password):  # If the user not exist or hash doesn't match
        return Response("Get out of here")

    response = Response(f"Hello, {user['name']}!<br />Balance: {user['balance']}", media_type='text/html')

    signed_login = base64.b64encode(login.encode()).decode() + "." + sign.sign_data(login)  # Signing cookies
    response.set_cookie(key="username", value=signed_login)

    return response
