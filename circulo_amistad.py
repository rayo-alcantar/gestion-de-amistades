# circulo_amistad.py

import os
import shutil
from amigo import Amigo

class CirculoAmistad:
    def __init__(self, nombre_archivo='amigos.txt', criterios=None):
        self.nombre_archivo = nombre_archivo
        self.criterios = criterios
        self.amigos = self.cargar_amigos()

    def cargar_amigos(self):
        """Carga los amigos desde un archivo, intentando UTF-8 primero y luego Latin-1."""
        amigos = []
        if not os.path.exists(self.nombre_archivo):
            return amigos

        content = ""
        encoding_used = 'utf-8'
        
        try:
            with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
                content = archivo.read()
        except UnicodeDecodeError:
            # Fallback a latin-1 si falla utf-8 (migración)
            try:
                with open(self.nombre_archivo, 'r', encoding='latin-1') as archivo:
                    content = archivo.read()
                encoding_used = 'latin-1'
            except Exception as e:
                print(f"Error crítico al leer archivo: {e}")
                return []

        # Procesar líneas
        lines = content.splitlines()
        for linea in lines:
            if not linea.strip():
                continue
            try:
                amigos.append(Amigo.from_line(linea, self.criterios))
            except ValueError as e:
                print(f"Error al procesar una línea: {e}")
        
        # Si se leyó con latin-1, forzar guardado en utf-8 inmediatamente para migrar
        if encoding_used == 'latin-1' and amigos:
            self.amigos = amigos # Asignar temporalmente para guardar
            self.guardar_amigos()
            
        return amigos

    def guardar_amigos(self):
        """Guarda todos los amigos en un archivo con codificación UTF-8 y crea backup."""
        # Crear backup si existe el archivo original
        if os.path.exists(self.nombre_archivo):
            try:
                shutil.copy2(self.nombre_archivo, self.nombre_archivo + ".bak")
            except IOError as e:
                print(f"No se pudo crear backup: {e}")

        try:
            with open(self.nombre_archivo, 'w', encoding='utf-8', newline='') as archivo:
                for amigo in self.amigos:
                    archivo.write(amigo.to_line() + '\n')
        except IOError as e:
             print(f"Error al guardar amigos: {e}")

    def agregar_amigo(self, nombre, puntuaciones, genero="M"):
        """
        Agrega un nuevo amigo al círculo y lo guarda.
        """
        nuevo_amigo = Amigo(nombre, puntuaciones, genero, criterios=self.criterios)
        self.amigos.append(nuevo_amigo)
        self.guardar_amigos()

    def reevaluar_amigo(self, indice, nuevas_puntuaciones, nuevo_nombre=None, nuevo_genero=None):
        """
        Reevaluar un amigo existente basado en nuevas puntuaciones y, opcionalmente, actualizar nombre y género.
        """
        try:
            amigo = self.amigos[indice]
            amigo.actualizar_puntuaciones(nuevas_puntuaciones)
            if nuevo_nombre and nuevo_nombre.strip() and nuevo_nombre.strip() != amigo.nombre:
                amigo.editar_nombre(nuevo_nombre)
            if nuevo_genero and nuevo_genero in ("M", "F") and nuevo_genero != amigo.genero:
                amigo.editar_genero(nuevo_genero)
            self.guardar_amigos()
            return True
        except IndexError:
            return False

    def eliminar_amigo(self, indice):
        """
        Elimina un amigo del círculo basado en su índice en la lista.
        """
        try:
            del self.amigos[indice]
            self.guardar_amigos()
            return True
        except IndexError:
            return False

    def listar_amigos(self):
        """Devuelve una lista de todos los amigos con sus detalles."""
        return [str(amigo) for amigo in self.amigos]

    def mostrar_circulo(self):
        """Devuelve una lista de amigos ordenados por puntuación total."""
        amigos_ordenados = sorted(self.amigos, key=lambda a: sum(a.puntuaciones.values()), reverse=True)
        return [(amigo.nombre,
                 sum(amigo.puntuaciones.values()),
                 amigo.categoria,
                 "Hombre" if amigo.genero == "M" else "Mujer")
                for amigo in amigos_ordenados]
