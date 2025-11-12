from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ruta principal
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "games": None})

# Ruta de búsqueda
@app.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, nombre: str = ""):
    if not nombre:
        return templates.TemplateResponse("index.html", {"request": request, "games": []})

    url = f"https://api.rawg.io/api/games?key=TU_API_KEY&search={nombre}"
    resp = requests.get(url)
    data = resp.json().get("results", [])

    return templates.TemplateResponse("index.html", {"request": request, "games": data})

