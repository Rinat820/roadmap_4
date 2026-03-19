import copy

from src.match_score.schemas import MatchScoreRequest
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
            "winner": {
                "id": None,
                "name": None
            }
        }
        logger.info(f"Match {uuid} created p1: {player1} p2: {player2}")
        return uuid
    
    @classmethod
    def add_point(cls, data: MatchScoreRequest):
        match = cls.matches.get(data.uuid)
        if not match:
            logger.warning(f"Match {data.uuid} not found")
            raise MatchNotFoundError("Данного матча не существует")
        
        if match["player1_id"] == data.winner_id:
            player_idx = 0
        elif match["player2_id"] == data.winner_id:
            player_idx = 1
        else:
            logger.warning(f"This player {data.winner_id} is not participating in this match {data.uuid}")
            raise PlayerNotParticipantError("Данный игрок не участвует в этом матче")
        

        match["score"]["points"][player_idx] += 1
        
        return cls._update_status(match, player_idx)
                                                 
    @staticmethod
    def _update_status(match, player_idx):
        score = match["score"]
        opponent = 1 - player_idx
        is_finished = False


        is_tb = (score["games"][0] == 6 and score["games"][1] == 6)
        point_limit = 7 if is_tb else 4

        if score["points"][player_idx] >= point_limit and (score["points"][player_idx] - score["points"][opponent] >= 2):
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
                match["winner"]["id"] = match[f"player{player_idx + 1}_id"]

                
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
            winner_id = match["winner"]["id"],
            score = match["score"]
        )
        
        logger.info(f"Match {uuid} removed. Winner ID: {match['winner_id']}")
        return data
    
    @staticmethod
    def format_score(match):
        mapping = {0: "0", 1: "15", 2: "30", 3: "40"}
        
        display_match = copy.deepcopy(match)
        if not display_match["score"]["games"] == [6, 6]:
            p1, p2 = display_match["score"]["points"]
            display_match["score"]["points"] = [
                mapping.get(p1, "AD"),
                mapping.get(p2, "AD")
            ]
        return display_match
    
