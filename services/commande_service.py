from sqlalchemy.orm import Session
from models.commande import Commande, StatutCommande
from datetime import datetime

def generer_ref(db: Session) -> str:
    annee = datetime.now().year
    
    debut_annee = datetime(annee, 1, 1)
    fin_annee = datetime(annee, 12, 31)
    
    count = db.query(Commande).filter (
        Commande.date_commande >= debut_annee,
        Commande.date_commande <= fin_annee
    ).count()
    
    numero = str(count + 1).zfill(2)
    
    return f"{annee}-{numero}"
    

def get_all(db: Session):
    
    return db.query(Commande).all()

def get_by_id(db: Session, Commande_id: int):
    
    return db.query(Commande).filter(Commande.id == Commande_id).first()

def create(db: Session, statut: StatutCommande, montant_total: float, client_id: int):
    
    reference = generer_ref(db)
    
    commande = Commande(reference=reference, statut=statut, montant_total=montant_total, client_id=client_id)
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

def modifier_statut(db: Session, Commande_id: int, statut: StatutCommande):
    commande = get_by_id(db, Commande_id)
    if commande:
        commande.statut = statut
        db.commit()
        db.refresh(commande)
    return commande