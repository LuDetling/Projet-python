from pydantic import BaseModel, field_validator, model_validator
from models.commande import StatutCommande

class CommandeCreate(BaseModel):
    client_id: int
    montant_total: float
    statut: str = "CREEE"

    @field_validator("client_id")
    @classmethod
    def valider_client_id(cls, valeur: int) -> int:
        if valeur <= 0:
            raise ValueError("L'identifiant client doit être un entier positif")
        return valeur

    @field_validator("montant_total")
    @classmethod
    def valider_montant(cls, valeur: float) -> float:
        if valeur <= 0:
            raise ValueError("Le montant doit être supérieur à 0")

        if valeur > 999999.99:
            raise ValueError("Le montant ne peut pas dépasser 999 999,99 €")

        # Arrondit à 2 décimales
        return round(valeur, 2)

    @field_validator("statut")
    @classmethod
    def valider_statut(cls, valeur: str) -> str:
        statuts_valides = [statut.name for statut in StatutCommande]  # ["CREEE", "CONFIRMEE", ...]

        if valeur not in statuts_valides:
            raise ValueError(f"Statut invalide. Valeurs acceptées : {', '.join(statuts_valides)}")

        return valeur


class CommandeUpdateStatut(BaseModel):
    statut: str

    @field_validator("statut")
    @classmethod
    def valider_statut(cls, valeur: str) -> str:
        statuts_valides = [statut.name for statut in StatutCommande]

        if valeur not in statuts_valides:
            raise ValueError(f"Statut invalide. Valeurs acceptées : {', '.join(statuts_valides)}")

        return valeur