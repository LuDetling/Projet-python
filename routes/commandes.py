from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from services import commande_service, client_service
from models.commande import StatutCommande

router = APIRouter(prefix="/commandes", tags=["commandes"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def liste_commandes(request: Request, db: Session = Depends(get_db)):
    commandes = commande_service.get_all(db)
    clients = client_service.get_all(db)
    return templates.TemplateResponse(
        request=request,
        name="commandes/liste.html",
        context={"commandes": commandes, "clients": clients}
    )
    
    
@router.post('/', response_class=HTMLResponse)
def creer_commande(
    request: Request,
    db: Session = Depends(get_db),
    client_id: int = Form(...),
    montant_total: float = Form(...),
    statut: str = Form("CREEE")
): 
    commande_service.create(
        db,
        client_id=client_id,
        montant_total=montant_total,
        statut=StatutCommande[statut]
    )
    commandes = commande_service.get_all(db)
    clients = client_service.get_all(db)
    return templates.TemplateResponse(
        request=request,
        name="commandes/_liste.html",
        context={
            "commandes": commandes,
            "clients": clients
        }
    )
    
@router.patch("/{commande_id}/statut", response_class=HTMLResponse)
def modifier_statut(
    request: Request,
    commande_id: int,
    statut: str = Form(...),
    db: Session = Depends(get_db)
):
    commande_service.modifier_statut(
        db,
        Commande_id=commande_id,
        statut=StatutCommande[statut]
    )
    commandes = commande_service.get_all(db)
    
    return templates.TemplateResponse(
        request=request,
        name="commandes/_liste.html",
        context={
            "commandes": commandes
        }
    )