from sqlalchemy.orm import Session
from models.client import Client

def get_all(db: Session):
    return db.query(Client).all()

def get_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def create(db: Session, nom: str, email: str, telephone: str = None, adresse: str = None):
    client = Client(nom=nom, email=email, telephone=telephone, adresse=adresse)
    db.add(client)      # prépare l'insertion
    db.commit()         # envoie à la base
    db.refresh(client)  # recharge l'objet avec l'id généré
    return client

def update(db: Session, client_id: int, nom: str, email: str, telephone: str = None, adresse: str = None):
    client = get_by_id(db, client_id)
    if not client:
        return
    
    client.nom = nom
    client.email = email
    client.telephone = telephone
    client.adresse = adresse
    
    db.commit()
    db.refresh(client)
    return client

def delete(db: Session, client_id: int):
    client = get_by_id(db, client_id)
    if client:
        db.delete(client)
        db.commit()
    return client
