import logging
import os


class Logger:
    def __init__(self, nameClass: str):
        env = os.environ.get('WEBAPP_ENV', 'dev')

        formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- {name}.%(message)s".format(name=nameClass))

        handler_info = logging.FileHandler("src/Logs/info.log", mode="a", encoding="utf-8")
        handler_error = logging.FileHandler("src/Logs/error.log", mode="a", encoding="utf-8")
        handler_debug = logging.FileHandler("src/Logs/debug.log", mode="a", encoding="utf-8")

        handler_info.setFormatter(formatter)
        handler_error.setFormatter(formatter)
        handler_debug.setFormatter(formatter)

        handler_info.setLevel(logging.INFO)
        handler_error.setLevel(logging.ERROR)
        handler_debug.setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)

        if env == 'dev':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.addHandler(handler_info)
        logger.addHandler(handler_error)
        logger.addHandler(handler_debug)

    def __formatMessage(self, nameMethod: str, message: str):
        return "{method} : {message}".format(method=nameMethod, message=message)

    def debug(self, nameMethod: str, message: str):
        self.logger.debug(self.__formatMessage(nameMethod, message))

    def info(self, nameMethod: str, message: str):
        self.logger.info(self.__formatMessage(nameMethod, message))

    def error(self, nameMethod: str, message: str):
        self.logger.error(self.__formatMessage(nameMethod, message))
