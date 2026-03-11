from src.new_match.handler import NewMatchHandler
from src.view.responses import ResponseBuilder

from src.error_handler import ErrorHandler


class NewMatchController:
    @staticmethod
    def render_page(environ: dict):
        try:
            return NewMatchHandler.render_page(environ)
        except Exception as e:
            status, error_text = ErrorHandler.error_handle(e)
            return ResponseBuilder.build_error_response(status, "new-match.html", error_text)
        
    @staticmethod
    def create_match(environ: dict):
        try:
            return NewMatchHandler.create_match(environ)
        except Exception as e:
            status, error_text = ErrorHandler.error_handle(e)
            return ResponseBuilder.build_error_response(status, "new-match.html", error_text)