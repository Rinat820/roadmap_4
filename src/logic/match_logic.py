from src.logic.dto import MatchDTO
from src.dao.dto import PlayerDTO

from src.exceptions import MatchNotFoundError, PlayerNotParticipantError

import logging


logger = logging.getLogger(__name__) 


class MatchManager:
    matches = {}
    
    @classmethod
    def create_match(cls, uuid, player1: PlayerDTO, player2: PlayerDTO):
        cls.matches[uuid] = {
            "player1_id": player1.id,
            "player2_id": player2.id,
            "player1_name": player1.name,
            "player2_name": player2.name,
            "score": {
                "sets": [0, 0],
                "games": [0, 0],
                "points": [0, 0]  
            },
            "winner_id": None
        }
        logger.info(f"Match {uuid} created p1: {player1} p2: {player2}")
        return uuid
    
    @classmethod
    def add_point(cls, uuid, winner):
        match = cls.matches.get(uuid)
        if not match:
            logger.warning(f"Match {uuid} not found")
            raise MatchNotFoundError("Данного матча не существует")
        
        if match["player1_id"] == winner:
            player_idx = 0
        elif match["player2_id"] == winner:
            player_idx = 1
        else:
            logger.warning(f"This player {winner} is not participating in this match {uuid}")
            raise PlayerNotParticipantError("Данный игрок не участвует в этом матче")
        

        match["score"]["points"][player_idx] += 1
        
        return cls._update_status(match, player_idx)
                                                 
    @classmethod
    def _update_status(cls, match, player_idx):
        score = match["score"]
        opponent = 1 - player_idx
        is_finished = False


        is_tb = (score["games"][0] == 6 and score["games"][1] == 6)
        point_limit = 7 if is_tb else 4

        if score["points"][player_idx] == point_limit:
            score["points"] = [0, 0]
            score["games"][player_idx] += 1
            

            if score["games"][player_idx] >= 6 and (score["games"][player_idx] - score["games"][opponent] >= 2):
                score["sets"][player_idx] += 1
                score["games"] = [0, 0]

            elif score["games"][player_idx] == 7:
                score["sets"][player_idx] += 1
                score["games"] = [0, 0]

            if score["sets"][player_idx] == 2:
                is_finished = True
                if player_idx == 0:
                    match["winner_id"] = match["player1_id"]
                if player_idx == 1:
                    match["winner_id"] = match["player2_id"]

                
        return is_finished, match
    
    @classmethod
    def finish_match(cls, uuid):
        match = cls.matches.pop(uuid, None)
        if match is None:
            logger.warning(f"Match {uuid} not found")
            raise MatchNotFoundError("Данного матча не существует")
        
        data = MatchDTO(
            uuid = uuid,
            player1_id = match["player1_id"],
            player2_id = match["player2_id"],
            winner_id = match["winner_id"],
            score = match["score"]
        )
        
        logger.info(f"Match {uuid} removed. Winner ID: {match['winner_id']}")
        return data
        