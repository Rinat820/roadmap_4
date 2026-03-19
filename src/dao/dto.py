from dataclasses import dataclass
from typing import List

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
    
@dataclass
class MatchViewDTO:
    id: int
    player1_name: str
    player2_name: str
    winner_name: str
    score: dict    

@dataclass
class MatchesPageDTO:
    matches: List[MatchViewDTO]
    total_pages: int  