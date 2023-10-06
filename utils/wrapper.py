# External libraries
import traceback

from functools import wraps

# Own libraries
from config import get_log


def router(func):
    @wraps(func)
    async def wrapper(**kwargs):
        response = kwargs['response']
        success = None
        data = None
        status_code = 200
        message = None

        try:
            data = func(**kwargs)
            message = 'Se obtuvo el resultado exitosamente.'
            success = True
        except Exception as e:
            log = get_log()
            log.error(traceback.format_exc())
            data = None
            message = 'Error al obtener el resultado'
            success = False
            status_code = 500
        finally:
            response.status_code = status_code
            res = dict(success=success, msg=message, data=data)

        return res

    return wrapper
