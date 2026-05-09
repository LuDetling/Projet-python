from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from services import commande_service

router = APIRouter(prefix="/commandes", tags=["commandes"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def liste_commandes(request: Request, db: Session = Depends(get_db)):
    commandes = commande_service.get_all(db)
    return templates.TemplateResponse(
        request=request,
        name="commandes/liste.html",
        context={"commandes": commandes}
    )