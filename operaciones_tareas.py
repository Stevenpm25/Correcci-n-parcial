from fastapi import HTTPException
import csv
import os
from datetime import datetime

RUTA_CSV_TAREAS = "tareas.csv"
ESTADOS_VALIDOS = {"Pendiente", "En ejecución", "Realizada", "Cancelada"}


def agregar_tarea(tarea: dict):
    if tarea["estado"] not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado inválido para la tarea.")

    archivo_existe = os.path.isfile(RUTA_CSV_TAREAS)
    with open(RUTA_CSV_TAREAS, mode="a", newline="", encoding="utf-8") as archivo:
        campos = ["id", "nombre", "descripcion", "fecha_creacion", "fecha_modificacion", "estado", "usuario"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if not archivo_existe:
            writer.writeheader()

        tarea["fecha_creacion"] = datetime.utcnow().isoformat()
        tarea["fecha_modificacion"] = tarea["fecha_creacion"]
        writer.writerow(tarea)


def obtener_tarea_por_id(tarea_id: int):
    try:
        with open(RUTA_CSV_TAREAS, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == tarea_id:
                    return dict(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de tareas no encontrado.")
    return None


def actualizar_estado_tarea(tarea_id: int, estado: str) -> bool:
    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado inválido para la tarea.")

    tareas_actualizadas = []
    tarea_encontrada = False

    try:
        with open(RUTA_CSV_TAREAS, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == tarea_id:
                    fila["estado"] = estado
                    fila["fecha_modificacion"] = datetime.utcnow().isoformat()
                    tarea_encontrada = True
                tareas_actualizadas.append(fila)

        if not tarea_encontrada:
            return False

        with open(RUTA_CSV_TAREAS, mode="w", newline="", encoding="utf-8") as archivo:
            campos = ["id", "nombre", "descripcion", "fecha_creacion", "fecha_modificacion", "estado", "usuario"]
            writer = csv.DictWriter(archivo, fieldnames=campos)
            writer.writeheader()
            writer.writerows(tareas_actualizadas)

        return True

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de tareas no encontrado.")


def obtener_todas_las_tareas():
    try:
        with open(RUTA_CSV_TAREAS, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            return list(reader)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de tareas no encontrado.")


def obtener_tareas_por_estado(estado: str):
    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado inválido para la búsqueda.")

    tareas = []
    try:
        with open(RUTA_CSV_TAREAS, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila["estado"] == estado:
                    tareas.append(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de tareas no encontrado.")
    return tareas


def obtener_tareas_por_usuario(usuario_id: int):
    tareas = []
    try:
        with open(RUTA_CSV_TAREAS, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["usuario"]) == usuario_id:
                    tareas.append(fila)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de tareas no encontrado.")
    return tareas

