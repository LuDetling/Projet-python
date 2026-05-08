from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    telephone: Mapped[Optional[str]] = mapped_column(String(20))
    adresse: Mapped[Optional[str]] = mapped_column(String(255))
    date_creation: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relation : Un client peut avoir plusieurs commandes
    commandes: Mapped[List["Commande"]] = relationship("Commande", back_populates="client")

    def __repr__(self) -> str:
        return f"<Client {self.nom}>"