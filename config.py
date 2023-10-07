import joblib
import logging
import os
import asyncio
from functools import lru_cache
from pydantic_settings import BaseSettings
import motor.motor_asyncio

from metadata.path import Path


class Settings(BaseSettings):
    app_name: str = 'LinkScribe-Blueprint'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_model() -> joblib:
    """Carga el modelo para predecir."""
    loaded_model = joblib.load(Path.modelo)
    return loaded_model


@lru_cache()
def get_vector_model() -> joblib:
    """Carga el modelo para predecir."""
    loaded_model = joblib.load(Path.vector)
    return loaded_model


@lru_cache()
def get_log():
    """Creación del logger de la aplicación"""
    return logging.getLogger('uvicorn.info')


@lru_cache()
def get_bd():

    mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb_uri')
    bd = client.predict_url

    return bd


@lru_cache()
def get_llaves_jwt() -> dict:
    """ Obtiene las llaves pública y privada para codificar y
    decodificar token jwt.

    Returns:
        Llaves pública y privada.

      ... code-block:: python

            {'private_jwt_key': 'vFivSFFFVbausuhgasdhjcxz',
            'public_jwt_key': 'achcibcew76yewhjcdsweISkjsj'}
    """

    with open(Path.private_key_jwt) as fname:
        private_jwt_pem = fname.read()

    with open(Path.public_key_jwt) as fname:
        public_jwt_pem = fname.read()

    keys = {'private_jwt_key': private_jwt_pem,
            'public_jwt_key': public_jwt_pem}

    return keys
