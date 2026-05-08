import enum
from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# Définition des statuts autorisés
class StatutCommande(enum.Enum):
    CREEE = "créée"
    CONFIRMEE = "confirmée"
    EXPEDIEE = "expédiée"
    LIVREE = "livrée"
    ANNULEE = "annulée"

class Commande(Base):
    __tablename__ = "commandes"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    date_commande: Mapped[datetime] = mapped_column(server_default=func.now())
    montant_total: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Statut limité au set défini dans l'Enum
    statut: Mapped[StatutCommande] = mapped_column(
        Enum(StatutCommande), 
        default=StatutCommande.CREEE
    )

    # Clé étrangère vers le client
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    
    # Relation : La commande appartient à un client
    client: Mapped["Client"] = relationship("Client", back_populates="commandes")

    def __repr__(self) -> str:
        return f"<Commande {self.reference} - {self.statut.value}>"