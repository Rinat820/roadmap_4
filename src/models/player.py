from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Player(Base):
    __tablename__ = "players"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False) 