import urllib.parse
import os
import traceback
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from bson import Binary
from fastapi.responses import JSONResponse, RedirectResponse

from utils.auth import cookie_required
from utils.predecir import predir_categoria
from utils.webscraping import web_scraping
from metadata.path import Path
from config import get_log, get_bd


log = get_log()
predicion_router = APIRouter(prefix='/predict', tags=['predict_router'])


templates = Jinja2Templates(directory='./public/static/html')


@predicion_router.get(
    "/form-listas", status_code=200)
async def form_predict(
        request: Request,
        url: str,
        user=Depends(cookie_required)):
    """

    """
    url = urllib.parse.unquote(url)
    try:
        mongo_bd = get_bd()
        user_collection = mongo_bd['listas']
        find_user = {'username': user}
        opciones = await user_collection.find_one(find_user)
        if opciones:
            opciones = opciones['listas'].keys()
        else:
            opciones = []
        data = web_scraping(url)
        if data:
            descripcion_web = data['description']

            data = {'title': data['title'], 'categoria': descripcion_web,
                    'img': data['main_image']}

            if descripcion_web != 'No se encontró una descripción.':
                data['categoria'] = predir_categoria(descripcion_web)

        else:
            raise ValueError('La url no es accesible.')

        data['request'] = request
        data['opciones'] = opciones
        respuesta = templates.TemplateResponse('formulario.html', data)
        respuesta.headers["Content-Type"] = "text/html"

    except Exception as e:
        msg = 'error desconocido'
        log.error(str(traceback.format_exc()))
        res = dict(success=False, data=None, msg=msg)
        respuesta = JSONResponse(content=res, status_code=500)

    return respuesta


@predicion_router.get(
    "/form-url", status_code=200)
async def form_predict(request: Request):
    """

    """

    respuesta = templates.TemplateResponse('formurl.html',
                                           {'request': request})

    return respuesta


@predicion_router.post(
    "/enviar-url", status_code=200)
async def enviar_url(request: Request):
    """

    """
    form_data = await request.form()
    url = form_data.get("url")
    url_codificada = urllib.parse.quote(url)

    return RedirectResponse("/predict/form-listas" + f"?url={url_codificada}",
                            status_code=302)


@predicion_router.post(
    "/enviar-prediccion",
    status_code=200)
async def enviar_prediccion(request: Request, user=Depends(cookie_required)):

    form_data = await request.form()

    ruta_img = f'{Path.public}/{form_data.get("ruta_img")}'

    with open(ruta_img, "rb") as imagen_binaria:
        datos_imagen = imagen_binaria.read()

    nuevo_dict = {
        "titulo": form_data.get('titulo'),
        "categoria": form_data.get('categoria'),
        "imagen": Binary(datos_imagen)
    }

    mongo_bd = get_bd()
    user_collection = mongo_bd['listas']
    find_user = {'username': user}
    listas = await user_collection.find_one(find_user)
    listas = listas['listas']
    opcion = form_data.get("lista")
    lista = listas.get(opcion)

    lista.append(nuevo_dict)
    user_collection.update_one(
        find_user, {"$set": {f"listas.{opcion}": lista}})

    if 'morfeo' not in ruta_img:
        os.remove(ruta_img)

    return RedirectResponse("/home/index",
                            status_code=302)

