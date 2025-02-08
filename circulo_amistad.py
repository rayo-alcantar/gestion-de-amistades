# circulo_amistad.py

import os
from amigo import Amigo

class CirculoAmistad:
	def __init__(self, nombre_archivo='amigos.txt'):
		self.nombre_archivo = nombre_archivo
		self.amigos = self.cargar_amigos()

	def cargar_amigos(self):
		"""Carga los amigos desde un archivo, si existe."""
		amigos = []
		if os.path.exists(self.nombre_archivo):
			with open(self.nombre_archivo, 'r', encoding='latin-1') as archivo:
				for linea in archivo:
					try:
						amigos.append(Amigo.from_line(linea))
					except ValueError as e:
						print(f"Error al procesar una línea: {e}")
		return amigos

	def guardar_amigos(self):
		"""Guarda todos los amigos en un archivo."""
		with open(self.nombre_archivo, 'w', encoding='latin-1') as archivo:
			for amigo in self.amigos:
				archivo.write(amigo.to_line() + '\n')

	def agregar_amigo(self, nombre, puntuaciones, genero="M"):
		"""
		Agrega un nuevo amigo al círculo y lo guarda.
		
		Se espera que el diccionario 'puntuaciones' tenga exactamente 10 claves,
		correspondientes a los siguientes criterios (evaluados del 1 al 10):
		
		  1. empatía_calidez  
		  2. confianza  
		  3. reciprocidad  
		  4. intereses_compartidos  
		  5. disponibilidad_presencia  
		  6. comunicacion_efectiva  
		  7. apoyo_dificultades  
		  8. resolucion_conflictos  
		  9. diversion_recreacion  
		  10. crecimiento_personal
		  
		Estos criterios buscan abarcar aspectos emocionales, prácticos y de crecimiento personal,
		de modo que la evaluación sea lo más completa y diferenciada posible.
		"""
		nuevo_amigo = Amigo(nombre, puntuaciones, genero)
		self.amigos.append(nuevo_amigo)
		self.guardar_amigos()

	def reevaluar_amigo(self, indice, nuevas_puntuaciones, nuevo_nombre=None, nuevo_genero=None):
		"""
		Reevaluar un amigo existente basado en nuevas puntuaciones y, opcionalmente, actualizar nombre y género.
		El parámetro 'indice' es la posición del amigo en la lista.
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
		Se asume que el índice es válido.
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
