from src.dao.base import BaseDAO
from src.models.match import Match


class MatchDAO(BaseDAO):
    model = Match
    