from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import Base ,engine
from models.client import Client
from models.commande import Commande, StatutCommande

with Session(engine) as session:
    try:
        nouveau_client = Client(
            nom='Detling',
            email='lucas.detling@gmail.com',
            telephone='0668372876',
            adresse='51 avenue de la république, 37100, Tours'
        )
        
        nouvelle_commande = Commande(
            reference='CMD-2026-01',
            montant_total=137.95,
            statut= StatutCommande.CONFIRMEE,
            client=nouveau_client
        )
        
        session.add(nouvelle_commande)
        session.commit()
        print("Données insérées !")
        
    except Exception as e:
        session.rollback()
        
with Session(engine) as session:
    client= session.query(Client).filter_by(nom='Detling').first()
    print(f"\nClient trouvé : {client.nom} (Inscrit le : {client.date_creation})")
    
    for cmd in client.commandes:
        print(f" - Commande {cmd.reference} : {cmd.montant_total}€ [Statut : {cmd.statut.value}]")