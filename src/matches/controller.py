from src.view.responses import ResponseBuilder
from src.matches.handler import MatchesHandler
from src.error_handler import ErrorHandler


class MatchesController:
    @staticmethod
    def get_matches_page(environ: dict):
        try:
            return MatchesHandler.get_matches_page(environ)
        except Exception as e:
            status, error_text = ErrorHandler.error_handle(e)
            return ResponseBuilder.build_error_response(status, "matches.html", error_text,
                                                        matches=[],
                                                        page=0,
                                                        total_pages=0,
                                                        filter_name=''
                                                        )