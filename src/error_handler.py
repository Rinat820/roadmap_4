from src.http_status import NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from src.exceptions import PlayerNameError, PageNumberError, MatchNotFoundError, PlayerNotParticipantError

import traceback
import logging


logger = logging.getLogger(__name__)


class ErrorHandler:
    @staticmethod
    def error_handle(exception):
        if isinstance(exception, (PlayerNameError, PageNumberError)):
            """Логгирование пути ошибок при валидации схем"""
            stack = traceback.extract_tb(exception.__traceback__)
            path_chain = " -> ".join([f"{f.filename.split('/')[-1]}:{f.name}" for f in stack])
            logger.warning(f"PATH: {path_chain} | MSG: {exception}")
            
            status, error_text = BAD_REQUEST, exception
        elif isinstance(exception, PlayerNotParticipantError):
            status, error_text = BAD_REQUEST, exception
        elif isinstance(exception, MatchNotFoundError):
            status, error_text = NOT_FOUND, exception
        else:
            logger.error('Server error', exc_info=True)
            status, error_text = SERVER_ERROR, exception
        return status, str(error_text)