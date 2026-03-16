from src.http_status import OK, SEE_OTHER

from src.handler import BaseHandler
from src.match_score.service import MatchScoreService
from src.view.responses import ResponseBuilder

from src.match_score.schemas import MatchScoreRequest


class MatchScoreHandler(BaseHandler):
    @classmethod
    def render_page(cls, environ: dict):
        query_data = cls._parse_query_params(environ)
        match_id = query_data.get("uuid", [''])[0]
        match = MatchScoreService.render_page(match_id)
        return ResponseBuilder.render(OK, "match-score.html", match=match, uuid=match_id, error='')
    
    @classmethod
    def process_point(cls, environ: dict):
        query_data = cls._parse_query_params(environ)
        form_data = cls._parse_form_data(environ)
        
        match_id = query_data.get("uuid", [''])[0]
        winner_id = int(form_data.get("winner_id", [''])[0])
        
        data = MatchScoreRequest(
            uuid=match_id,
            winner_id=winner_id
        )
        is_finished, match = MatchScoreService.process_point(data)
        
        if is_finished:
            return ResponseBuilder.redirect(SEE_OTHER, "/matches")
        return ResponseBuilder.render(OK, "match-score.html", match=match, uuid=match_id, error='')
        
        