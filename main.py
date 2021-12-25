import os
import base64

from typing import Optional
from fastapi import FastAPI, Request, Response, Form, Cookie
from fastapi.templating import Jinja2Templates

from auth_error import AuthError
from sign import Sign

app = FastAPI()
templates = Jinja2Templates(directory="templates")
KEY = os.environ['KEY']
sign = Sign(key=KEY)
auth = AuthError()

users = {
    'Alex@user.com': {
        'name': 'Alex',
        'password': 'Password',
        'balance': 100_000
    },
    'Petr@user.com': {
        'name': 'Petr',
        'password': 'pass123',
        'balance': 200_000
    }
}


@app.get("/")
async def index(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:
        return templates.TemplateResponse("auth.html", context={"request": request})

    valid_username = sign.get_username_from_signed_string(username)

    if not valid_username:
        auth.redirect_to_auth_form(context={"request": request})

    try:
        user = users[valid_username]
    except KeyError:
        auth.redirect_to_auth_form(context={"request": request})

    return Response(f"Hello, {users[valid_username]['name']}")


@app.post("/login")
async def login(login: str = Form(...), password: str = Form(...)):
    user = users.get(login)

    if not user or user["password"] != password:
        return Response("Get out of here")

    response = Response(f"Hello, {user['name']}!<br />Balance: {user['balance']}", media_type='text/html')

    signed_login = base64.b64encode(login.encode()).decode() + "." + sign.sign_data(login)
    response.set_cookie(key="username", value=signed_login)

    return response
