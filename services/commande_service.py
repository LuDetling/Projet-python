from sqlalchemy.orm import Session
from models.commande import Commande, StatutCommande

def get_all(db: Session):
    return db.query(Commande).all()

def get_by_id(db: Session, Commande_id: int):
    return db.query(Commande).filter(Commande.id == Commande_id).first()

def create(db: Session, reference: str, statut: StatutCommande, montant_total: float):
    commande = Commande(reference=reference, statut=statut, montant_total=montant_total)
    db.add(commande)      # prépare l'insertion
    db.commit()         # envoie à la base
    db.refresh(commande)  # recharge l'objet avec l'id généré
    return commande

def delete(db: Session, Commande_id: int):
    commande = get_by_id(db, Commande_id)
    if commande:
        db.delete(commande)
        db.commit()
    return commande