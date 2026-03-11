from uuid import uuid4

from src.dao.player import PlayerDAO

from src.logic.match_logic import MatchManager

from src.models.player import Player
from src.new_match.schemas import CreateMatchRequest


class NewMatchService:
    @staticmethod 
    def start_match(data: CreateMatchRequest) -> str:
        new_uuid = str(uuid4())
        player1_id = PlayerDAO.get_or_create(data.player1)
        player2_id = PlayerDAO.get_or_create(data.player2)
        
        match_id = MatchManager.create_match(new_uuid, player1_id, player2_id)
        
        return match_id