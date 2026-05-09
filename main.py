from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import engine, Base
from routes import clients, commandes

# Crée toutes les tables au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mon App MVC")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
    

# Enregistre les routes
app.include_router(clients.router)
app.include_router(commandes.router)