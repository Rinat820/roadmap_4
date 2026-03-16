from dataclasses import dataclass

@dataclass
class MatchScoreRequest:
    uuid: str
    winner_id: int