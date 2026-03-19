from sqlalchemy import select, or_, func
from sqlalchemy.future import select
from src.database import session_maker

from src.dao.base import BaseDAO
from src.models.match import Match
from src.dao.dto import MatchDTO, MatchesPageDTO, MatchViewDTO


class MatchDAO(BaseDAO):
    model = Match
    dto = MatchDTO
    
    @classmethod
    def get_matches_page(cls, page: int, page_size: int, player_name: str = None) -> MatchesPageDTO:
        offset = (page - 1) * page_size
        
        with session_maker() as session:
            query = select(cls.model)

            if player_name:
                from src.models.player import Player

                query = query.join(Player, or_(
                    cls.model.player1_id == Player.id, 
                    cls.model.player2_id == Player.id
                )).where(Player.name.ilike(f"%{player_name}%")).distinct()

            total_count = session.scalar(select(func.count()).select_from(query.subquery()))
            total_pages = (total_count + page_size - 1) // page_size

            results = session.scalars(query.limit(page_size).offset(offset)).all()
                        
            matches = []
            for row in results:
                matches.append(MatchViewDTO(
                    id=row.id,
                    player1_name=row.player1.name,
                    player2_name=row.player2.name,
                    winner_name=row.winner.name if row.winner else "No winner",
                    score=row.score
                ))
            
            data = MatchesPageDTO(
                matches=matches,
                total_pages=total_pages
            )
            
            return data