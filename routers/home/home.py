from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from config import get_log

from utils.auth import cookie_required, decode_time_token


log = get_log()
home_router = APIRouter(prefix='/home', tags=['home_router'])


templates = Jinja2Templates(directory='./public/static/html')


@home_router.get(
    "/index", status_code=200)
async def home(request: Request, auth: str):
    """

    """
    data = cookie_required(auth)
    respuesta = templates.TemplateResponse('home.html',
                                           {'request': request})

    return respuesta
