from database import Base
from sqlalchemy import create_engine
from models.client import Client
from models.commande import Commande

engine = create_engine("sqlite:///mini_app.db")

# Crée toutes les tables définies dans Base
Base.metadata.create_all(engine)