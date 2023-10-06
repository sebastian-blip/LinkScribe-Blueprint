import urllib.parse
import base64
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from config import get_log, get_bd


from utils.auth import cookie_required, create_time_token, decode_time_token


log = get_log()
listas_router = APIRouter(prefix='/listas', tags=['listas_router'])


templates = Jinja2Templates(directory='./public/static/html')


@listas_router.get(
    "/form-listas", status_code=200, dependencies=[Depends(cookie_required)])
async def agregar_lista(
        request: Request,
        verificado: str = 'No',
        lista_guard: str = 'no'):

    respuesta = templates.TemplateResponse(
        'formlistas.html',
        {'request': request,
         'verificado': verificado,
         'lista_guard': lista_guard
         }
    )

    return respuesta


@listas_router.post(
    "/agregar-listas", status_code=200)
async def agregar_lista(request: Request, user=Depends(cookie_required)):
    """

    """
    mongo_bd = get_bd()
    user_collection = mongo_bd['listas']
    find_user = {'username': user}
    data_listas = await user_collection.find_one(find_user)

    form_data = await request.form()

    if data_listas:
        listas = data_listas['listas'].keys()
        if form_data.get('nombre') in listas:
            response = RedirectResponse(
                "/listas/form-listas" + f"?verificado=si",
                status_code=302)
        else:
            actualizacion = {
                "$set": {
                    f'listas.{form_data.get("nombre")}': []
                }
            }
            user_collection.update_one(find_user, actualizacion)

            response = RedirectResponse(
                "/listas/form-listas" + f"?lista_guard=si",
                status_code=302)
    else:
        create_lista = {
            "username": user,
            'listas': {form_data.get('nombre'): []}
        }
        await user_collection.insert_one(create_lista)
        response = RedirectResponse(
            "/listas/form-listas" + f"?lista_guard=si",
            status_code=302)

    return response


@listas_router.get(
    "/buscar-lista", status_code=200)
async def form_predict(request: Request, user=Depends(cookie_required)):
    """

    """

    mongo_bd = get_bd()
    user_collection = mongo_bd['listas']
    find_user = {'username': user}
    opciones = await user_collection.find_one(find_user)
    opciones = opciones['listas'].keys()

    respuesta = templates.TemplateResponse(
        'buscarlista.html',
        {
            'request': request,
            'opciones': opciones
        }
    )

    return respuesta


@listas_router.get(
    "/mostrar-lista", status_code=200)
async def busar_lista(request: Request,
                      opcion: str,
                      user=Depends(cookie_required)):
    """

    """
    mongo_bd = get_bd()
    user_collection = mongo_bd['listas']
    find_user = {'username': user}
    listas = await user_collection.find_one(find_user)
    listas = listas['listas']
    lista = listas.get(opcion)

    listas_usuarios = []
    for lis in lista:
        imagen = lis['imagen']
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        lis['imagen'] = imagen_base64
        listas_usuarios.append(lis)

    data = {'listas': listas_usuarios, 'opcion': opcion, 'request': request}

    respuesta = templates.TemplateResponse(
        'mostarlistasusuario.html',
        data
    )

    return respuesta


@listas_router.post(
    "/enviar-lista", status_code=200)
async def enviar_lista(request: Request):
    """

    """
    form_data = await request.form()
    opcion = form_data.get("lista")

    return RedirectResponse("/listas/mostrar-lista" + f"?opcion={opcion}",
                            status_code=302)


@listas_router.get(
    "/crear-url-compartir", status_code=200)
async def url_lista_compartida(request: Request, data: str, user=Depends(cookie_required)):
    """

    """

    token = create_time_token(user, data)
    url = request.base_url
    url = f'{url}listas/lista-compartida?token={token}'

    return templates.TemplateResponse(
        'urlcompartida.html',
        {'url': url,
         'request': request}
    )


@listas_router.get(
    "/lista-compartida", status_code=200)
async def url_lista_compartida(request: Request, token: str):
    """

    """
    data = decode_time_token(token)

    mongo_bd = get_bd()
    user_collection = mongo_bd['listas']
    find_user = {'username': data['username']}
    listas = await user_collection.find_one(find_user)
    listas = listas['listas']
    lista = listas.get(data['lista'])

    listas_usuarios = []
    for lis in lista:
        imagen = lis['imagen']
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        lis['imagen'] = imagen_base64
        listas_usuarios.append(lis)

    data = {
        'listas': listas_usuarios,
        'opcion': data['lista'],
        'user': data['username'],
        'request': request}

    respuesta = templates.TemplateResponse(
        'lista_compartida.html',
        data
    )

    return respuesta

