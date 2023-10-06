# External libraries
import os
import uvicorn

from fastapi import Depends
from fastapi import FastAPI, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Union

# Own libraries
from config import Settings, get_settings
from metadata.sesion import Sesion
from utils.auth import decode_token


app = FastAPI(
    title='LinkScribe-Blueprint',
    version='0.1.0')

app.mount("/static", StaticFiles(directory="public/static",  html=True), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for root, dirs, files in os.walk('routers'):
    if '__' not in root:
        path = root.split(os.sep)
        for file in files:
            if '__' not in file:
                file, _ = os.path.splitext(file)
                path_import = f'{".".join(path)}.{file}'
                module = __import__(path_import, globals(), locals(), [f'{file}_router'])
                router = getattr(module, f'{file}_router')
                app.include_router(router)


@app.get('/info')
async def info(settings: Settings = Depends(get_settings)):
    return dict(settings)


if __name__ == '__main__':
    uvicorn.run(app)
