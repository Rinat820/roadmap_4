from src.match_score.handler import MatchScoreHandler
from src.view.responses import ResponseBuilder

from src.error_handler import ErrorHandler


class MatchScoreController:
    @staticmethod
    def render_page(environ: dict):
        try:
            return MatchScoreHandler.render_page(environ)
        except Exception as e:
            status, error_text = ErrorHandler.error_handle(e)
            return ResponseBuilder.build_error_response(status, "new-match.html", error_text)
    
    @staticmethod
    def process_point(environ: dict):
        try:
            return MatchScoreHandler.process_point(environ)
        except Exception as e:
            status, error_text = ErrorHandler.error_handle(e)
            return ResponseBuilder.build_error_response(status, "new-match.html", error_text)