#!/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from flask_marshmallow import Marshmallow


db = SQLAlchemy()

ma = Marshmallow()

env = os.environ.get('WEBAPP_ENV', 'dev')

# logging
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

handler_critic = logging.FileHandler("src/Logs/critic.log", mode="a", encoding="utf-8")
handler_info = logging.FileHandler("src/Logs/info.log", mode="a", encoding="utf-8")
handler_error = logging.FileHandler("src/Logs/error.log", mode="a", encoding="utf-8")
handler_debug = logging.FileHandler("src/Logs/debug.log", mode="a", encoding="utf-8")

handler_critic.setFormatter(formatter)
handler_info.setFormatter(formatter)
handler_error.setFormatter(formatter)
handler_debug.setFormatter(formatter)

handler_info.setLevel(logging.INFO)
handler_critic.setLevel(logging.CRITICAL)
handler_error.setLevel(logging.ERROR)
handler_debug.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

if env == 'dev':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)
logger.addHandler(handler_critic)
logger.addHandler(handler_info)
logger.addHandler(handler_error)
logger.addHandler(handler_debug)
