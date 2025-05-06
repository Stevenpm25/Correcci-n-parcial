from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from operaciones_usuarios import *

app = FastAPI()

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    premium: bool = False
    estado: bool = False

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    agregar_usuario(usuario.dict())
    return {"mensaje": "Usuario agregado correctamente"}

@app.get("/usuarios")
def listar_usuarios():
    return obtener_usuario()
@app.get("/usuarios/activos")
def listar_usuarios_activos():
    return obtener_usuarios_activos()

@app.get("/usuarios/premium-activos")
def listar_usuarios_premium_activos():
    return obtener_usuarios_premium_activos()
@app.get("/usuarios/{usuario_id}")
def obtener_usuario_por_id_route(usuario_id: int):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/usuarios/{usuario_id}/estado")
def actualizar_estado_usuario_route(usuario_id: int, estado: bool):
    exito = actualizar_usuario_estado(usuario_id, estado)
    if exito:
        return {"mensaje": f"El usuario ha sido {'activado' if estado else 'desactivado'} correctamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/usuarios/{usuario_id}/premium")
def actualizar_premium_usuario_route(usuario_id: int, premium: bool):
    exito = actualizar_usuario_premium(usuario_id, premium)
    if exito:
        return {"mensaje": f"Usuario {'promovido a premium' if premium else 'retirado de premium'} correctamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


RUTA_CSV_TAREAS = "tareas.csv"
class Tarea(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str = Field(..., pattern="^(Pendiente|En ejecución|Realizada|Cancelada)$")
    usuario: int

@app.post("/tareas/")
def crear_tarea(tarea: Tarea):
    agregar_tarea(tarea.dict())
    return {"mensaje": "Tarea creada correctamente"}

@app.get("/tareas/")
def listar_todas_las_tareas():
    return obtener_todas_las_tareas()

@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    tarea = obtener_tarea_por_id(tarea_id)
    if tarea:
        return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.patch("/tareas/{tarea_id}/estado")
def cambiar_estado_tarea(
    tarea_id: int,
    estado: str = Query(..., pattern="^(Pendiente|En ejecución|Realizada|Cancelada)$")
):
    exito = actualizar_estado_tarea(tarea_id, estado)
    if exito:
        return {"mensaje": f"Estado actualizado a '{estado}' correctamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.get("/tareas/estado/{estado}")
def tareas_por_estado(estado: str):
    return obtener_tareas_por_estado(estado)

@app.get("/tareas/usuario/{usuario_id}")
def tareas_por_usuario(usuario_id: int):
    return obtener_tareas_por_usuario(usuario_id)

@app.patch("/tareas/{tarea_id}/editar")
def editar_tarea(
    tarea_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None
):
    tarea = obtener_tarea_por_id(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    tareas = obtener_todas_las_tareas()
    tarea_encontrada = False

    for t in tareas:
        if int(t["id"]) == tarea_id:
            if nombre:
                t["nombre"] = nombre
            if descripcion:
                t["descripcion"] = descripcion
            t["fecha_modificacion"] = datetime.utcnow().isoformat()
            tarea_encontrada = True
            break

    if not tarea_encontrada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    with open(RUTA_CSV_TAREAS, mode="w", newline="", encoding="utf-8") as archivo:
        campos = ["id", "nombre", "descripcion", "fecha_creacion", "fecha_modificacion", "estado", "usuario"]
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(tareas)

    return {"mensaje": "Tarea actualizada correctamente"}