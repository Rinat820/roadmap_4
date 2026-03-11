from src.router import Router

from src.logger_config import setup_logging


setup_logging()
routing = Router()


def application(environ, start_response):
    return routing.handle_request(environ, start_response)
