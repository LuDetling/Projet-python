from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from database import get_db
from services import client_service
from schemas.client_schema import ClientCreate, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def liste_clients(request: Request, db: Session = Depends(get_db)):
    clients = client_service.get_all(db)
    return templates.TemplateResponse(
        request=request,
        name="clients/liste.html",
        context={"clients": clients}   # ← les variables du template ici
    )

@router.post("/", response_class=HTMLResponse)
def creer_client(
    request: Request,
    nom: str = Form(...),
    email: str = Form(...),
    telephone: str = Form(""),
    adresse: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        data = ClientCreate(
            nom=nom,
            email=email,
            telephone=telephone,
            adresse=adresse,
        )

        client_service.create(db, nom=data.nom, email=data.email, telephone=data.telephone, adresse=data.adresse)
        clients = client_service.get_all(db)
        response =  templates.TemplateResponse(
            request=request,
            name="clients/_liste.html",
            context={"clients": clients}
        )
        response.headers["HX-Trigger"] = '{"notification": {"type": "succes", "message": "Client créé avec succès"}}'
        return response
        
    except ValidationError as e:
        # Récupère le premier message d'erreur Pydantic
        premier_message = e.errors()[0]["msg"].replace("Value error, ", "")
        return templates.TemplateResponse(
            request=request,
            name="_erreur.html",
            context={"message": premier_message},
            status_code=422,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )

    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse(
            request=request,
            name="_erreur.html",
            context={"message": "Cet email est déjà utilisé par un autre client"},
            status_code=409,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )
     
@router.get("/{client_id}/modifier", response_class=HTMLResponse)
def form_modifier_client(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    client = client_service.get_by_id(db, client_id)
    if not client:
        return templates.TemplateResponse(
            request=request,
            name="_erreur.html",
            context={"message": "Client introuvable"},
            status_code=404,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )
    return templates.TemplateResponse(
        request=request,
        name="clients/_form_modifier.html",
        context={"client": client}
    )
        
@router.patch("/{client_id}/modifier", response_class=HTMLResponse)
def modifier_client(
    request: Request,
    client_id: int,
    nom: str = Form(...),
    email: str = Form(...),
    telephone: str = Form(None),
    adresse: str = Form(None),
    db: Session = Depends(get_db)
): 
    try:
        data = ClientUpdate(
            client_id=client_id,
            nom=nom,
            email=email,
            telephone=telephone,
            adresse=adresse
        )
        
        client_service.update(
            db,
            client_id=data.client_id,
            nom=data.nom,
            email=data.email,
            telephone=data.telephone,
            adresse=data.adresse
        )
        clients = client_service.get_all(db)
        response =  templates.TemplateResponse(
            request=request,
            name="clients/liste.html",
            context={"clients": clients}
        )
        response.headers["HX-Trigger"] = '{"notification": {"type": "succes", "message": "Client créé avec succès"}}'
        return response
    
    except ValidationError as e:
        premier_message = e.errors()[0]["msg"].replace("Value error, ", "")
        return templates.TemplateResponse(
            request=request,
            name="_erreur.html",
            context={"message": premier_message},
            status_code=422,
            headers={"HX-Retarget": "#notifications", "HX-Reswap": "innerHTML"}
        )