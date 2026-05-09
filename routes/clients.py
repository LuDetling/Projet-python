from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from services import client_service

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
    client_service.create(db, nom=nom, email=email, telephone=telephone, adresse=adresse)
    clients = client_service.get_all(db)
    return templates.TemplateResponse(
        request=request,
        name="clients/_liste.html",
        context={"clients": clients}
    )