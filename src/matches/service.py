from src.dao.match import MatchDAO
from src.dao.dto import MatchesPageDTO

from src.matches.schemas import MatchesRequest


class MatchesService:
    @staticmethod
    def get_matches_page(data: MatchesRequest) -> MatchesPageDTO:
        return MatchDAO.get_matches_page(
            page=data.page_number,
            page_size=5,
            player_name=data.player_name
        )