from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re

class ClientCreate(BaseModel):
    nom: str
    email: EmailStr  # Pydantic vérifie le format email automatiquement
    telephone: str | None = None
    adresse: str | None = None

    # Valide un seul champ
    @field_validator("nom")
    @classmethod
    def valider_nom(cls, valeur: str) -> str:
        valeur = valeur.strip()  # supprime les espaces en début/fin

        if len(valeur) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")

        if len(valeur) > 100:
            raise ValueError("Le nom ne peut pas dépasser 100 caractères")

        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", valeur):
            raise ValueError("Le nom ne peut contenir que des lettres, espaces, tirets et apostrophes")

        return valeur.title()  # "jean dupont" → "Jean Dupont"

    @field_validator("telephone")
    @classmethod
    def valider_telephone(cls, valeur: str | None) -> str | None:
        if valeur is None:
            return None

        # Supprime espaces, tirets, points
        nettoye = re.sub(r"[\s\-\.]", "", valeur)

        if not re.match(r"^(\+33|0)[1-9](\d{8})$", nettoye):
            raise ValueError("Format téléphone invalide (ex: 06 12 34 56 78 ou +33612345678)")

        return nettoye  # stocke le numéro nettoyé

    @field_validator("adresse")
    @classmethod
    def valider_adresse(cls, valeur: str | None) -> str | None:
        if valeur is None:
            return None

        valeur = valeur.strip()
        if len(valeur) < 5:
            raise ValueError("L'adresse doit contenir au moins 5 caractères")

        return valeur


class ClientUpdate(BaseModel):
    """Pour les modifications partielles — tous les champs sont optionnels"""
    nom: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    adresse: str | None = None

    # model_validator : valide plusieurs champs ensemble
    @model_validator(mode="after")
    def au_moins_un_champ(self) -> "ClientUpdate":
        champs = [self.nom, self.email, self.telephone, self.adresse]
        if all(c is None for c in champs):
            raise ValueError("Au moins un champ doit être fourni pour la mise à jour")
        return self