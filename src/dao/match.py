from src.dao.base import BaseDAO
from src.models.match import Match
from src.dao.dto import MatchDTO


class MatchDAO(BaseDAO):
    model = Match
    dto = MatchDTO
    