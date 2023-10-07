# External libraries
import jwt
from datetime import datetime, timedelta
from fastapi import Cookie
from fastapi.exceptions import HTTPException
from typing import Union


# Own libraries
from config import get_llaves_jwt
from metadata.sesion import Sesion


def create_access_token(user: str) -> jwt:
    """Crea un token de inicio de sección para el usuario válido.

    Args:
        user: usuario válido al que pertenece el token.
        hours: tiempo en horas de validez del token.

     Returns:
         token asociado al usuario.

    """

    keys = get_llaves_jwt()
    secret_key = keys['private_jwt_key']
    data = {
        'user_id': None,
        'username': user,
        'exp': datetime.utcnow() + timedelta(hours=Sesion.expiracion_token),
    }

    return jwt.encode(data, secret_key, algorithm='RS512')


def decode_token(token: str) -> dict:
    """Función para decodificar el token.

    Args:
        token: Token a decodificar.

    Returns:
        datos del usuario al que pertenece el token

        .. code-block:: python

           {
             'user_id': None,
             'username': user}

    """

    keys = get_llaves_jwt()
    try:
        secret_key = keys['public_jwt_key']
        message = jwt.decode(token, secret_key, algorithms=['RS512'])
        respuesta = dict(success=True, msg=message)
    except jwt.ExpiredSignatureError:
        respuesta = dict(success=False, msg='Token ha caducado')
    except jwt.InvalidTokenError:
        respuesta = dict(success=False, msg='La sesión no es válida.')
    except Exception as e:
        respuesta = dict(success=False, msg=f'Error desconocido: {e}')

    return respuesta


def create_time_token(user: str, lista: str) -> jwt:
    """Crea un token de inicio de sección para el usuario válido.

    Args:
        user: usuario válido al que pertenece el token.
        hours: tiempo en horas de validez del token.

     Returns:
         token asociado al usuario.

    """

    keys = get_llaves_jwt()
    secret_key = keys['private_jwt_key']
    data = {
        'username': user,
        'exp': datetime.utcnow() + timedelta(hours=Sesion.expiracion_time),
        'lista': lista
    }

    return jwt.encode(data, secret_key, algorithm='RS512')


async def decode_time_token(token: str):
    """Verifica la autorización del token y permite el paso a los endpoint.

    Args:
        token: que contiene la informacion de la lista a compartir.

    Returns:
        retorna la data de la lsita

    """

    data_user = decode_token(token)
    if not data_user['success']:
        return HTTPException(status_code=401, detail=data_user['msg'])

    return data_user['msg']


async def cookie_required(
        auth: Union[str, None] = Cookie(default=None, alias=Sesion.cookie_name)):
    """Verifica la autorización del cookie y permite el paso a los endpoint.

    Args:
        auth: Cookie correspondiente a la información del usuario.

    Returns:
        retorna la misma cookie con la información del usuario si fue validada
        correctamente.

    """
    print(auth)
    data_user = decode_token(auth)
    print(data_user)
    if not data_user['success']:
        raise HTTPException(status_code=401, detail=data_user['msg'])

    user_name = data_user['msg'].get('username')

    return user_name
