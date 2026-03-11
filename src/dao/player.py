from src.dao.base import BaseDAO
from src.models.player import Player

from src.dao.dto import PlayerDTO


class PlayerDAO(BaseDAO):
    model = Player
    dto = PlayerDTO
    
    @classmethod
    def get_or_create(cls, name) -> PlayerDTO:
        player = cls.find_one_or_none(name=name)
        if not player:
            player = cls.add(name=name)
        return player