from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBUsuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)
    premium = Column(Boolean, default=False)
    estado = Column(Boolean, default=False)

class DBTarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    estado = Column(String)
    usuario_id = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    premium: bool = False
    estado: bool = False

class Tarea(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str = Field(..., pattern="^(Pendiente|En ejecución|Realizada|Cancelada)$")
    usuario: int

def agregar_usuario(usuario: dict):
    db = SessionLocal()
    db_usuario = DBUsuario(**usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    db.close()

def obtener_usuario():
    db = SessionLocal()
    usuarios = db.query(DBUsuario).all()
    db.close()
    return usuarios

def obtener_usuarios_activos():
    db = SessionLocal()
    usuarios = db.query(DBUsuario).filter(DBUsuario.estado == True).all()
    db.close()
    return usuarios

def obtener_usuarios_premium_activos():
    db = SessionLocal()
    usuarios = db.query(DBUsuario).filter(DBUsuario.estado == True, DBUsuario.premium == True).all()
    db.close()
    return usuarios

def obtener_usuario_por_id(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(DBUsuario).filter(DBUsuario.id == usuario_id).first()
    db.close()
    return usuario

def actualizar_usuario_estado(usuario_id: int, estado: bool):
    db = SessionLocal()
    usuario = db.query(DBUsuario).filter(DBUsuario.id == usuario_id).first()
    if usuario:
        usuario.estado = estado
        db.commit()
        db.close()
        return True
    db.close()
    return False

def actualizar_usuario_premium(usuario_id: int, premium: bool):
    db = SessionLocal()
    usuario = db.query(DBUsuario).filter(DBUsuario.id == usuario_id).first()
    if usuario:
        usuario.premium = premium
        db.commit()
        db.close()
        return True
    db.close()
    return False

def agregar_tarea(tarea: dict):
    db = SessionLocal()
    db_tarea = DBTarea(
        id=tarea["id"],
        nombre=tarea["nombre"],
        descripcion=tarea["descripcion"],
        estado=tarea["estado"],
        usuario_id=tarea["usuario"]
    )
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    db.close()

def obtener_todas_las_tareas():
    db = SessionLocal()
    tareas = db.query(DBTarea).all()
    db.close()
    return tareas

def obtener_tarea_por_id(tarea_id: int):
    db = SessionLocal()
    tarea = db.query(DBTarea).filter(DBTarea.id == tarea_id).first()
    db.close()
    return tarea

def actualizar_estado_tarea(tarea_id: int, estado: str):
    db = SessionLocal()
    tarea = db.query(DBTarea).filter(DBTarea.id == tarea_id).first()
    if tarea:
        tarea.estado = estado
        db.commit()
        db.close()
        return True
    db.close()
    return False

def obtener_tareas_por_estado(estado: str):
    db = SessionLocal()
    tareas = db.query(DBTarea).filter(DBTarea.estado == estado).all()
    db.close()
    return tareas

def obtener_tareas_por_usuario(usuario_id: int):
    db = SessionLocal()
    tareas = db.query(DBTarea).filter(DBTarea.usuario_id == usuario_id).all()
    db.close()
    return tareas

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
    db = SessionLocal()
    tarea = db.query(DBTarea).filter(DBTarea.id == tarea_id).first()
    if not tarea:
        db.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if nombre:
        tarea.nombre = nombre
    if descripcion:
        tarea.descripcion = descripcion

    db.commit()
    db.close()
    return {"mensaje": "Tarea actualizada correctamente"}