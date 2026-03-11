from dataclasses import dataclass

@dataclass
class MatchDTO:
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: int
    score: dict | list