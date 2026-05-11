from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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
    try: 
        if montant_total <= 0:
            raise ValueError("Le montant total doit être suppérieur à 0")
    
        commande_service.create(
            db,
            client_id=client_id,
            montant_total=montant_total,
            statut=StatutCommande[statut]
        )
        
        commandes = commande_service.get_all(db)
        clients = client_service.get_all(db)
        response = templates.TemplateResponse(
            request=request,
            name="commandes/_liste.html",
            context={
                "commandes": commandes,
                "clients": clients
            }
        )
        response.headers["HX-Trigger"] = '{"notification": {"type": "succes", "message": "Commande créée avec succès"}}'
        return response
    
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name="_errors.html",
            context={"message": str(e)},
            status_code=422,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )
        
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="_errors.html",
            context={"message": "une commande avec cette référence existe déjà"},
            status_code=409,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )
        
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="_errors.html",
            context={"message": "Une erreur innatendue s'est produite"},
            status_code=409,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )
    
    
    
@router.patch("/{commande_id}/statut", response_class=HTMLResponse)
def modifier_statut(
    request: Request,
    commande_id: int,
    statut: str = Form(...),
    db: Session = Depends(get_db)
):
    try: 
        commande = commande_service.modifier_statut(
            db,
            Commande_id=commande_id,
            statut=StatutCommande[statut]
        )
        
        if not commande:
            raise ValueError("Commande introuvable")
            
        commandes = commande_service.get_all(db)
        response = templates.TemplateResponse(
            request=request,
            name="commandes/_liste.html",
            context={
                "commandes": commandes
            }
        )
        response.headers["HX-Trigger"] = '{"notification": {"type": "succes", "message": "Statut mis à jour"}}'
        return response
    
    except KeyError:
        return templates.TemplateResponse(
            request=request,
            name="_erreur.html",
            context={"message": f"Statut '{statut}' invalide"},
            status_code=422,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )