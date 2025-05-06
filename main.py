from typing import Optional

from fastapi import *
from pydantic import BaseModel
from operaciones import *

app = FastAPI()

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    premium: bool = False
    estado: bool = False

@app.post("/Crear usuarios/")
def crear_usuario(usuario: Usuario):
    # Agregar el usuario al archivo CSV
    agregar_usuario(usuario.dict())
    return {"mensaje": "Usuario agregado correctamente"}

@app.get("/Obtener todos los usuarios/")
def listar_usuarios():
    # Listar todos los usuarios
    return obtener_usuario()

@app.get("/Obtener usuario por id/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/usuarios/{usuario_id}/estado")
def actualizar_estado_usuario(usuario_id: int, estado: bool):
    # Actualizar el estado del usuario
    exito = actualizar_usuario_estado(usuario_id, estado)
    if exito:
        return {"mensaje": f"El usuario ha sido {'activado' if estado else 'desactivado'} correctamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/usuarios/{usuario_id}/premium")
def hacer_usuario_premium(usuario_id: int, premium: bool):
    # Actualizar el estado premium del usuario
    exito = actualizar_usuario_premium(usuario_id, premium)
    if exito:
        return {"mensaje": f"Usuario {'promovido a premium' if premium else 'retirado de premium'} correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
@app.get("/usuarios/activos")
def listar_usuarios_activos():
    return obtener_usuarios_activos()
@app.get("/usuarios/premium-activos")
def listar_usuarios_premium_activos():
    return obtener_usuarios_premium_activos()