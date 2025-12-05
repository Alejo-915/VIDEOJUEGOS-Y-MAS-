 🚀 GUÍA COMPLETA PARA CREAR PROYECTO FASTAPI

**Guía paso a paso para crear un proyecto completo con FastAPI en 3 horas - Sin frameworks CSS complicados**

---

## 📋 Tabla de Contenidos

1. [Configuración Inicial](#-1-configuración-inicial)
2. [Estructura del Proyecto](#-2-estructura-del-proyecto)
3. [Código Backend](#-3-código-backend)
4. [Código Frontend](#-4-código-frontend)
5. [Comandos Git](#-5-comandos-git)
6. [Despliegue en Render](#-6-despliegue-en-render)
7. [Comandos Rápidos](#-7-comandos-rápidos)

---

## 🔧 1. Configuración Inicial

### Paso 1: Crear el proyecto
```bash
# Crear carpeta del proyecto
mkdir MiProyecto
cd MiProyecto

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias básicas
pip install fastapi uvicorn sqlmodel python-dotenv

# Crear archivo de dependencias
pip freeze > requirements.txt
```

### Paso 2: Crear archivo `.gitignore`
```gitignore
.venv/
__pycache__/
*.pyc
.env
*.db
```

### Paso 3: Crear archivo `.env`
```env
DATABASE_URL=sqlite:///database.db
```

---

## 📁 2. Estructura del Proyecto

Crea esta estructura de carpetas y archivos:
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
```

---

## 💻 3. Código Backend

### `database.py`
```python
from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

### `models.py`
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: float
    cantidad: int = 0
    activo: bool = True
```

---

### `routes/items.py` - CRUD Completo
```python
from fastapi import APIRouter, Depends, HTTPException
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

# DELETE (Soft Delete)
@router.delete("/{id}")
def eliminar_item(id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    item.activo = False
    session.add(item)
    session.commit()
    return {"mensaje": "Item eliminado correctamente"}
```

---

### `routes/pages.py`
```python
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

---

### `main.py`
```python
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
from routes import items, pages

app = FastAPI(title="Mi Proyecto API")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir routers
app.include_router(items.router)
app.include_router(pages.router)

# Endpoint de prueba
@app.get("/api")
def api_root():
    return {"mensaje": "API funcionando correctamente"}
```

---

## 🎨 4. Código Frontend (Simple y Bonito)

### `templates/index.html`
```html



    
    
    Mi Proyecto
    


    
        🚀 Mi Proyecto
        Sistema de Gestión
    

    
        
            
                Lista de Items
                + Nuevo Item
            

            
                Cargando...
            
        
    

    
    
        
            &times;
            Nuevo Item
            
            
                Nombre:
                

                Descripción:
                

                Precio:
                

                Cantidad:
                

                Guardar
                Cancelar
            
        
    

    


```

---

### `static/css/style.css`
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    text-align: center;
}

header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

header p {
    font-size: 1rem;
    opacity: 0.9;
}

.container {
    max-width: 1000px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.header-section h2 {
    color: #333;
}

/* Botones */
.btn-primary {
    background-color: #667eea;
    color: white;
    padding: 0.7rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
}

.btn-primary:hover {
    background-color: #5568d3;
}

.btn-secondary {
    background-color: #6c757d;
    color: white;
    padding: 0.7rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    margin-left: 0.5rem;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.btn-danger:hover {
    background-color: #c82333;
}

/* Cards de Items */
.item-card {
    background: white;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.item-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.item-info h3 {
    margin-bottom: 0.5rem;
    color: #333;
}

.item-info p {
    color: #666;
    font-size: 0.9rem;
}

.item-details {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.badge {
    background-color: #667eea;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
}

.badge-secondary {
    background-color: #6c757d;
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}

.modal-content {
    background-color: white;
    margin: 5% auto;
    padding: 2rem;
    border-radius: 10px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #000;
}

/* Formulario */
form {
    margin-top: 1rem;
}

label {
    display: block;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

input:focus {
    outline: none;
    border-color: #667eea;
}

form button {
    margin-top: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
    .item-card {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .item-details {
        margin-top: 1rem;
        width: 100%;
        justify-content: space-between;
    }
    
    .header-section {
        flex-direction: column;
        gap: 1rem;
    }
}
```

---

### `static/js/main.js`
```javascript
let items = [];

// Cargar items desde la API
async function cargarItems() {
    try {
        const response = await fetch('/items/');
        items = await response.json();
        mostrarItems();
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('items-container').innerHTML = 
            'Error al cargar items';
    }
}

// Mostrar items en el HTML
function mostrarItems() {
    const container = document.getElementById('items-container');
    
    if (items.length === 0) {
        container.innerHTML = 'No hay items disponibles';
        return;
    }
    
    container.innerHTML = items.map(item => `
        
            
                ${item.nombre}
                ${item.descripcion}
            
            
                $${item.precio.toFixed(2)}
                Cant: ${item.cantidad}
                Eliminar
            
        
    `).join('');
}

// Abrir modal
function mostrarModal() {
    document.getElementById('modal').style.display = 'block';
}

// Cerrar modal
function cerrarModal() {
    document.getElementById('modal').style.display = 'none';
    limpiarFormulario();
}

// Limpiar formulario
function limpiarFormulario() {
    document.getElementById('nombre').value = '';
    document.getElementById('descripcion').value = '';
    document.getElementById('precio').value = '';
    document.getElementById('cantidad').value = '';
}

// Guardar item
async function guardarItem() {
    const item = {
        nombre: document.getElementById('nombre').value,
        descripcion: document.getElementById('descripcion').value,
        precio: parseFloat(document.getElementById('precio').value),
        cantidad: parseInt(document.getElementById('cantidad').value)
    };
    
    // Validación
    if (!item.nombre || !item.descripcion || isNaN(item.precio) || isNaN(item.cantidad)) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    try {
        const response = await fetch('/items/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        });
        
        if (response.ok) {
            alert('Item creado exitosamente');
            cerrarModal();
            cargarItems();
        } else {
            alert('Error al crear el item');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

// Eliminar item
async function eliminarItem(id) {
    if (!confirm('¿Eliminar este item?')) return;
    
    try {
        const response = await fetch(`/items/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
            alert('Item eliminado');
            cargarItems();
        } else {
            alert('Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target == modal) {
        cerrarModal();
    }
}

// Cargar items al iniciar
cargarItems();
```

---

## 📦 5. Comandos Git

### Configuración inicial de Git
```bash
# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Initial commit: Proyecto FastAPI completo"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/tu-usuario/tu-repositorio.git

# Cambiar a rama main
git branch -M main

# Subir código
git push -u origin main
```

### Comandos Git comunes
```bash
# Ver estado de archivos
git status

# Agregar archivos específicos
git add nombre-archivo.py

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push

# Descargar cambios
git pull

# Ver historial
git log --oneline

# Crear nueva rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout main
```

---

## 🌐 6. Despliegue en Render

### Paso 1: Preparar el proyecto

Asegúrate de tener el archivo `requirements.txt` actualizado:
```bash
pip freeze > requirements.txt
```

### Paso 2: Crear cuenta en Render

1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta (puedes usar GitHub)

### Paso 3: Crear Web Service

1. Click en **"New"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Configura el servicio:
```
Name: mi-proyecto
Region: Oregon (o el más cercano)
Branch: main
Root Directory: (dejar vacío)
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port $PORT
```

4. Plan: **Free**
5. Click en **"Create Web Service"**

### Paso 4: Variables de Entorno (opcional)

Si usas PostgreSQL en producción:

1. Ve a **"Environment"**
2. Agrega: `DATABASE_URL` = `tu-url-de-postgres`

### Paso 5: Esperar el despliegue

- El primer despliegue toma 2-5 minutos
- Render te dará una URL: `https://tu-proyecto.onrender.com`

---

## ⚡ 7. Comandos Rápidos

### Desarrollo Local
```bash
# Activar entorno virtual
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload

# Ver documentación API
http://127.0.0.1:8000/docs
```

### Producción
```bash
# Actualizar requirements
pip freeze > requirements.txt

# Git
git add .
git commit -m "Update"
git push

# Render se actualiza automáticamente
```

---

## 📚 Recursos Adicionales

- **FastAPI Docs**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **SQLModel Docs**: [https://sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- **Render Docs**: [https://render.com/docs](https://render.com/docs)

---

## ✅ Checklist para el Parcial (3 horas)

- [ ] **0-15 min**: Crear entorno virtual, instalar dependencias, estructura de carpetas
- [ ] **15-45 min**: Implementar backend (database.py, models.py, routes/items.py, main.py)
- [ ] **45-90 min**: Crear frontend (HTML, CSS, JS) - Lo más que toma
- [ ] **90-105 min**: Probar localmente, arreglar errores
- [ ] **105-120 min**: Git init, commit, crear repo en GitHub
- [ ] **120-150 min**: Subir a GitHub, desplegar en Render
- [ ] **150-180 min**: Verificar que funcione, ajustes finales

---

## 🎯 Tips para el Parcial

1. **Copia y pega rápido**: No escribas todo desde cero
2. **Prueba cada parte**: Backend primero, luego frontend
3. **No te compliques**: Este código es simple y funcional
4. **Git frecuente**: Haz commits cada 30 minutos
5. **Render tarda**: Despliega con tiempo de sobra

---

**¡Listo para sacar 5.0! 🚀 Todo este código es simple, funcional y se ve bien sin parecer IA.**

**Tiempo estimado**: 2.5 - 3 horas  
**Dificultad**: Media  
**Stack**: FastAPI + SQLModel + HTML + CSS + JavaScript
