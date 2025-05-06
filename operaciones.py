from fastapi import *
import csv
import os


RUTA_CSV = "persistencia.csv"

def agregar_usuario(usuario: dict):
    archivo_existe = os.path.isfile(RUTA_CSV)
    with open(RUTA_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        # Asegúrate de incluir 'estado' y 'premium' en el archivo de nuevo usuario.
        campos = ["id", "nombre", "email", "estado", "premium"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if not archivo_existe:
            writer.writeheader()  # Solo si es la primera vez
        writer.writerow(usuario)



def obtener_usuario_por_id(usuario_id: int):
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == usuario_id:
                    return dict(fila)
    except FileNotFoundError:
        pass
    return None
def obtener_usuario_por_id(usuario_id: int):
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == usuario_id:
                    return dict(fila)
    except FileNotFoundError:
        pass
    return None
def actualizar_usuario_estado(usuario_id: int, estado: bool) -> bool:
    usuarios_actualizados = []
    usuario_encontrado = False

    try:
        # Leer el archivo CSV para buscar el usuario
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if int(fila["id"]) == usuario_id:
                    fila["estado"] = "True" if estado else "False"  # Actualizar el campo 'estado'
                    usuario_encontrado = True
                usuarios_actualizados.append(fila)

        if not usuario_encontrado:
            return False  # Si no se encuentra el usuario

        # Escribir los usuarios actualizados en el archivo CSV
        with open(RUTA_CSV, mode="w", encoding="utf-8", newline="") as archivo:
            fieldnames = ["id", "nombre", "email", "estado", "premium"]
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(usuarios_actualizados)

        return True
    except FileNotFoundError:
        return False  # Si no se encuentra el archivo

def actualizar_usuario_premium(usuario_id: int, premium: bool) -> bool:
    usuarios = []
    try:
        # Leer los usuarios desde el archivo CSV persistente
        with open(RUTA_CSV, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                usuarios.append(row)

        # Buscar el usuario por ID y actualizar su estado 'premium'
        for usuario in usuarios:
            if int(usuario['id']) == usuario_id:
                usuario['premium'] = 'True' if premium else 'False'
                break
        else:
            return False  # Si no se encuentra el usuario, retornamos False

        # Escribir los usuarios actualizados de vuelta en el archivo CSV
        with open(RUTA_CSV, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'nombre', 'email', 'estado', 'premium']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(usuarios)

        return True
    except FileNotFoundError:
        return False
def obtener_usuarios_activos():
    usuarios = []
    try:
        with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila.get("estado", "").lower() == "true":
                    usuarios.append(fila)
    except FileNotFoundError:
        pass
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
        pass
    return usuarios
