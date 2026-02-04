from src.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import CHAR, ForeignKey, JSON


class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    UUID: Mapped[str] = mapped_column(CHAR(36), unique=True)
    Player1: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Player2: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Winner: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Score: Mapped[list|dict] = mapped_column(JSON)
    
    
    
