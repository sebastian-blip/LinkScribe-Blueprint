from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from config import get_log

from utils.auth import cookie_required


log = get_log()
home_router = APIRouter(prefix='/home', tags=['home_router'])


templates = Jinja2Templates(directory='./public/static/html')


@home_router.get(
    "/index", status_code=200, dependencies=[Depends(cookie_required)])
async def home(request: Request):
    """

    """

    respuesta = templates.TemplateResponse('home.html',
                                           {'request': request})

    return respuesta
