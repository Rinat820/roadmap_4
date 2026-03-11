import re
from dataclasses import dataclass

from src.exceptions import PlayerNameError

@dataclass
class CreateMatchRequest:
    player1: str
    player2: str
    
    
    def __post_init__(self):
        if self.player1 == self.player2:
            raise PlayerNameError("Имена игроков не должны совпадать")
        
        if not re.fullmatch(r'(?=.{3,20}$)[A-Z][a-z]*', self.player1):
            raise PlayerNameError("Имя игрока должно быть в формате 'Name' (от 3 до 20 латинских символов)")
        if not re.fullmatch(r'(?=.{3,20}$)[A-Z][a-z]*', self.player2):
            raise PlayerNameError("Имя игрока должно быть в формате 'Name' (от 3 до 20 латинских символов)")