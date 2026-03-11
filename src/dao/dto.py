from dataclasses import dataclass

@dataclass
class PlayerDTO:
    id: int
    name: str
    
@dataclass
class MatchDTO:
    id: int
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: int
    score: dict