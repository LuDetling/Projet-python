from fastapi import Depends
from sqlalchemy.orm import Session
from database import Base ,engine
from models.client import Client
from models.commande import Commande, StatutCommande
from services.commande_service import generer_ref
from database import get_db


with Session(engine) as session:
    try:
        nouveau_client = Client(
            nom='Detling',
            email='lucas.detling@gmail.com',
            telephone='0668372876',
            adresse='51 avenue de la république, 37100, Tours'
        )
        db: Session = Depends(get_db)
        reference = generer_ref(db)
        
        nouvelle_commande = Commande(
            reference=reference,
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