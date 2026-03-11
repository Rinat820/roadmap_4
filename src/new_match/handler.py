from src.http_status import OK, SEE_OTHER

from src.handler import BaseHandler
from src.view.responses import ResponseBuilder
from src.new_match.service import NewMatchService

from src.new_match.schemas import CreateMatchRequest


class NewMatchHandler(BaseHandler):
    @staticmethod
    def render_page(environ: dict):
        return ResponseBuilder.render(OK, "new-match.html", error="")
    
    @classmethod
    def create_match(cls, environ: dict):
        form_data = cls._parse_form_data(environ)
        player1 = form_data.get('player1', [''])[0]
        player2 = form_data.get('player2', [''])[0]
        
        data = CreateMatchRequest(
            player1=player1,
            player2=player2
        )
        
        match_uuid = NewMatchService.start_match(data)
        
        return ResponseBuilder.redirect(SEE_OTHER, f"/match-score?uuid={match_uuid}")