from fastapi import HTTPException
import csv
import os
from operaciones_tareas import *
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

RUTA_CSV = "usuarios.csv"

def agregar_usuario(usuario: dict):
    archivo_existe = os.path.isfile(RUTA_CSV)
    with open(RUTA_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        campos = ["id", "nombre", "email", "estado", "premium"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if not archivo_existe:
            writer.writeheader()
        writer.writerow(usuario)


def obtener_usuario_por_id(usuario_id: int):
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == usuario_id:
                    return dict(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")
    return None


def actualizar_usuario_estado(usuario_id: int, estado: bool) -> bool:
    usuarios_actualizados = []
    usuario_encontrado = False

    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == usuario_id:
                    fila["estado"] = "True" if estado else "False"
                    usuario_encontrado = True
                usuarios_actualizados.append(fila)

        if not usuario_encontrado:
            return False

        with open(RUTA_CSV, mode="w", encoding="utf-8", newline="") as archivo:
            fieldnames = ["id", "nombre", "email", "estado", "premium"]
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(usuarios_actualizados)

        return True

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")


def actualizar_usuario_premium(usuario_id: int, premium: bool) -> bool:
    usuarios = []
    try:
        with open(RUTA_CSV, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                usuarios.append(row)

        for usuario in usuarios:
            if int(usuario['id']) == usuario_id:
                usuario['premium'] = 'True' if premium else 'False'
                break
        else:
            return False

        with open(RUTA_CSV, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'nombre', 'email', 'estado', 'premium']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(usuarios)

        return True
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")


def obtener_usuarios_activos():
    usuarios = []
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila.get("estado", "").lower() == "true":
                    usuarios.append(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")
    return usuarios


def obtener_usuarios_premium_activos():
    usuarios = []
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila.get("estado", "").lower() == "true" and fila.get("premium", "").lower() == "true":
                    usuarios.append(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")
    return usuarios


def obtener_usuario():
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            return list(reader)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

