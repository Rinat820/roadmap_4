from typing import Optional
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, ForeignKey, JSON

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.player import Player
    
    
class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False)
    
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"), nullable=True)
    
    score: Mapped[dict] = mapped_column(JSON, default=lambda: {})

    player1: Mapped["Player"] = relationship("Player", foreign_keys=[player1_id])
    player2: Mapped["Player"] = relationship("Player", foreign_keys=[player2_id])
    winner: Mapped[Optional["Player"]] = relationship("Player", foreign_keys=[winner_id])
