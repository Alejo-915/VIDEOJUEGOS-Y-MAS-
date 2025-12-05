GUÍA COMPLETA PARA EL PARCIAL FINAL

📋 PARTE 1: CONFIGURACIÓN INICIAL (5 minutos)
1. Crear el proyecto desde cero
bash# Crear carpeta del proyecto
mkdir MiProyecto
cd MiProyecto

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias básicas
pip install fastapi uvicorn sqlmodel python-dotenv
pip freeze > requirements.txt
2. Inicializar Git
bashgit init
git add .
git commit -m "Initial commit"
```

---

## 📁 **PARTE 2: ESTRUCTURA BÁSICA DEL PROYECTO**

Crea esta estructura de carpetas:
```

MiProyecto/
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
├── routes/
│   ├── items.py
│   └── pages.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js

💾 PARTE 3: CÓDIGO BASE (Copy-Paste)
database.py
pythonfrom sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
models.py (Ejemplo simple)
pythonfrom sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: float
    cantidad: int = 0
    activo: bool = True
routes/items.py (CRUD completo)
pythonfrom fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Item

router = APIRouter(prefix="/items", tags=["Items"])

# CREATE
@router.post("/")
def crear_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# READ ALL
@router.get("/")
def listar_items(session: Session = Depends(get_session)):
    return session.exec(select(Item).where(Item.activo == True)).all()

# READ ONE
@router.get("/{id}")
def obtener_item(id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

# UPDATE
@router.patch("/{id}")
def actualizar_item(id: int, datos: Item, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(item, key, value)
    
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# DELETE
@router.delete("/{id}")
def eliminar_item(id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    item.activo = False
    session.add(item)
    session.commit()
    return {"mensaje": "Item eliminado"}
routes/pages.py
pythonfrom fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
main.py
pythonfrom dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
from routes import items, pages

app = FastAPI(title="Mi Proyecto API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(items.router)
app.include_router(pages.router)

@app.get("/api")
def api_root():
    return {"mensaje": "API funcionando correctamente"}

🎨 PARTE 4: FRONTEND SIMPLE Y BONITO
templates/index.html
html<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Proyecto</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar is-primary">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
                <i class="fas fa-rocket"></i> &nbsp; <strong>Mi Proyecto</strong>
            </a>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero is-info">
        <div class="hero-body">
            <p class="title">Bienvenido a Mi Proyecto</p>
            <p class="subtitle">Sistema de gestión completo con FastAPI</p>
        </div>
    </section>

    <!-- Contenido Principal -->
    <section class="section">
        <div class="container">
            <h2 class="title">Items Disponibles</h2>
            
            <!-- Botón Crear -->
            <button class="button is-primary mb-4" onclick="mostrarModalCrear()">
                <i class="fas fa-plus"></i> &nbsp; Nuevo Item
            </button>

            <!-- Tabla de Items -->
            <div id="items-container">
                <p class="has-text-centered">Cargando...</p>
            </div>
        </div>
    </section>

    <!-- Modal Crear/Editar -->
    <div class="modal" id="modal-item">
        <div class="modal-background" onclick="cerrarModal()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Nuevo Item</p>
                <button class="delete" onclick="cerrarModal()"></button>
            </header>
            <section class="modal-card-body">
                <div class="field">
                    <label class="label">Nombre</label>
                    <input class="input" type="text" id="nombre" placeholder="Nombre del item">
                </div>
                <div class="field">
                    <label class="label">Descripción</label>
                    <input class="input" type="text" id="descripcion" placeholder="Descripción">
                </div>
                <div class="field">
                    <label class="label">Precio</label>
                    <input class="input" type="number" id="precio" placeholder="0.00" step="0.01">
                </div>
                <div class="field">
                    <label class="label">Cantidad</label>
                    <input class="input" type="number" id="cantidad" placeholder="0">
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-success" onclick="guardarItem()">Guardar</button>
                <button class="button" onclick="cerrarModal()">Cancelar</button>
            </footer>
        </div>
    </div>

    <script src="/static/js/main.js"></script>
</body>
</html>
static/css/style.css
cssbody {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.section {
    background: white;
    border-radius: 10px;
    margin: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.item-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.item-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
static/js/main.js
javascriptlet items = [];

async function cargarItems() {
    try {
        const response = await fetch('/items/');
        items = await response.json();
        mostrarItems();
    } catch (error) {
        console.error('Error:', error);
    }
}

function mostrarItems() {
    const container = document.getElementById('items-container');
    
    if (items.length === 0) {
        container.innerHTML = '<p class="has-text-centered">No hay items disponibles</p>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="item-card">
            <div class="columns is-vcentered">
                <div class="column">
                    <h3 class="title is-4">${item.nombre}</h3>
                    <p>${item.descripcion}</p>
                </div>
                <div class="column is-narrow">
                    <span class="tag is-large is-info">$${item.precio}</span>
                    <span class="tag is-large">Cant: ${item.cantidad}</span>
                </div>
                <div class="column is-narrow">
                    <button class="button is-danger" onclick="eliminarItem(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function mostrarModalCrear() {
    document.getElementById('modal-item').classList.add('is-active');
}

function cerrarModal() {
    document.getElementById('modal-item').classList.remove('is-active');
}

async function guardarItem() {
    const item = {
        nombre: document.getElementById('nombre').value,
        descripcion: document.getElementById('descripcion').value,
        precio: parseFloat(document.getElementById('precio').value),
        cantidad: parseInt(document.getElementById('cantidad').value)
    };
    
    try {
        const response = await fetch('/items/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        });
        
        if (response.ok) {
            alert('¡Item creado!');
            cerrarModal();
            cargarItems();
        }
    } catch (error) {
        alert('Error al crear item');
    }
}

async function eliminarItem(id) {
    if (!confirm('¿Eliminar este item?')) return;
    
    try {
        await fetch(`/items/${id}`, { method: 'DELETE' });
        alert('Item eliminado');
        cargarItems();
    } catch (error) {
        alert('Error al eliminar');
    }
}

// Cargar items al iniciar
cargarItems();
```

---

## 🌐 **PARTE 5: SUBIR A GITHUB Y RENDER**

### **.gitignore**
```
.venv/
__pycache__/
*.pyc
.env
*.db
Subir a GitHub:
bash# En GitHub, crea un nuevo repositorio (sin README)

git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main
Desplegar en Render:

Ve a render.com
Clic en "New" → "Web Service"
Conecta tu repositorio de GitHub
Configuración:

Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT


Clic en "Create Web Service"


⚡ COMANDOS RÁPIDOS PARA EL PARCIAL
bash# Iniciar proyecto
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn sqlmodel python-dotenv

# Ejecutar localmente
uvicorn main:app --reload

# Git
git init
git add .
git commit -m "Initial commit"
git remote add origin URL
git push -u origin main

# Ver API docs
http://127.0.0.1:8000/docs
