import json
from dataclasses import asdict

from src.exceptions import MatchNotFoundError

from src.match_score.schemas import MatchScoreRequest
from src.dao.match import MatchDAO
from src.logic.match_logic import MatchManager
from src.exceptions import MatchCompletedError

import logging


logger = logging.getLogger(__name__)


class MatchScoreService:
    @staticmethod
    def render_page(match_id: str):
        match = MatchManager.matches.get(match_id)
        if not match:
            logger.warning(f"Match {match_id} not found")
            raise MatchNotFoundError("Данного матча не существует")
        return MatchManager.format_score(match)
    
    @staticmethod
    def process_point(data: MatchScoreRequest):
        if MatchDAO.find_one_or_none(uuid=data.uuid):
            logger.warning(f"Match {data.uuid} is already completed. Scoring ignored")
            raise MatchCompletedError("Этот матч уже завершен")
        
        is_finished, match = MatchManager.add_point(data)
        display_match = MatchManager.format_score(match)
        if is_finished:
            new_data = MatchManager.finish_match(data.uuid)
            match_dict = asdict(new_data)
            match_dict['score'] = json.dumps(match_dict['score'])
            MatchDAO.add(**match_dict)
        
        return is_finished, display_match