from src.http_status import OK

from src.handler import BaseHandler
from src.matches.service import MatchesService
from src.view.responses import ResponseBuilder

from src.matches.schemas import MatchesRequest


class MatchesHandler(BaseHandler):
    @classmethod
    def get_matches_page(cls, environ: dict):
        query_data = cls._parse_query_params(environ)
        page_number=query_data.get("page", ['1'])[0]
        player_name=query_data.get("filter_by_player_name", [''])[0]
        
        data = MatchesRequest(
            page_number=page_number,
            player_name=player_name
        )
        
        new_data = MatchesService.get_matches_page(data)
        
        return ResponseBuilder.render(OK, "matches.html", error='',
                                matches=new_data.matches,
                                page=int(page_number),
                                total_pages=new_data.total_pages,
                                filter_name=player_name
                               )