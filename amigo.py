# amigo.py

class Amigo:
	def __init__(self, nombre, puntuaciones=None, genero="M", categoria=None):
		"""
		:param nombre: Nombre del amigo.
		:param puntuaciones: Diccionario con las puntuaciones; si no se proporciona se inicializa en 0.
		:param genero: 'M' para Hombre o 'F' para Mujer. Por defecto es 'M'.
		:param categoria: Categoría del amigo; si no se especifica se asigna "Desconocido".
		"""
		self.nombre = nombre.strip()
		self.puntuaciones = puntuaciones if puntuaciones else {
			"tiempo_compartido": 0,
			"apoyo_emocional": 0,
			"intereses_comunes": 0,
			"frecuencia_comunicacion": 0,
			"confianza": 0,
			"reciprocidad": 0,
			"resolucion_conflictos": 0,
			"inversion_personal": 0,
			"comprension_mutua": 0,
			"diversion_compartida": 0
		}
		# Normalizamos: si se recibe "H" se trata como "M"
		gen = genero.upper().strip()
		if gen == "H":
			gen = "M"
		self.genero = gen if gen in ("M", "F") else "M"
		self.categoria = categoria or "Desconocido"
		self.clasificar_amigo()

	def actualizar_puntuaciones(self, nuevas_puntuaciones):
		"""Actualiza las puntuaciones del amigo basándose en un diccionario de nuevas puntuaciones."""
		for clave, valor in nuevas_puntuaciones.items():
			if clave in self.puntuaciones and 1 <= valor <= 10:
				self.puntuaciones[clave] = valor
		self.clasificar_amigo()

	def clasificar_amigo(self):
		"""Clasifica al amigo en una categoría basada en su puntuación total."""
		puntuacion_total = sum(self.puntuaciones.values())
		if puntuacion_total > 90:
			self.categoria = "Súper Amigo"
		elif puntuacion_total >= 80:
			self.categoria = "Primario"
		elif puntuacion_total >= 60:
			self.categoria = "Secundario"
		elif puntuacion_total >= 40:
			self.categoria = "Terciario"
		elif puntuacion_total >= 20:
			self.categoria = "Ocasional"
		else:
			self.categoria = "Conocido"

	def editar_nombre(self, nuevo_nombre):
		"""Permite editar el nombre del amigo."""
		self.nombre = nuevo_nombre.strip()

	def editar_genero(self, nuevo_genero):
		"""Permite editar el género del amigo.
		
		Se espera que nuevo_genero sea 'M' o 'F'. Si se pasa otro valor, se asigna 'M' por defecto.
		"""
		nuevo_genero = nuevo_genero.upper().strip()
		if nuevo_genero not in ("M", "F"):
			nuevo_genero = "M"
		self.genero = nuevo_genero

	def __str__(self):
		detalles = f"Nombre: {self.nombre}\n"
		detalles += f"Género: {'Hombre' if self.genero == 'M' else 'Mujer'}\n"
		detalles += "\n".join([f"{clave.replace('_', ' ').title()}: {valor}" 
							   for clave, valor in self.puntuaciones.items()])
		detalles += f"\nCategoría: {self.categoria}\n"
		return detalles

	def to_line(self):
		"""
		Convierte la información del amigo en una línea de texto para el archivo,
		en el formato: Nombre, punt1, punt2, ..., punt10, Género, Categoría
		"""
		punt_str = ",".join(str(val) for val in self.puntuaciones.values())
		return f"{self.nombre},{punt_str},{self.genero},{self.categoria}"

	@staticmethod
	def from_line(line):
		"""
		Crea un objeto Amigo a partir de una línea de texto.
		Se espera que la línea tenga:
		 - 13 campos: [nombre, 10 puntuaciones, género, categoría]  
		 o  
		 - 12 campos: [nombre, 10 puntuaciones, género+categoría]
		   en cuyo caso se toma el primer carácter como género (y se normaliza: "H"→"M")
		   y el resto como categoría.
		"""
		parts = line.strip().split(',')
		if len(parts) == 13:
			nombre = parts[0]
			scores = list(map(int, parts[1:11]))
			puntuaciones = {
				"tiempo_compartido": scores[0],
				"apoyo_emocional": scores[1],
				"intereses_comunes": scores[2],
				"frecuencia_comunicacion": scores[3],
				"confianza": scores[4],
				"reciprocidad": scores[5],
				"resolucion_conflictos": scores[6],
				"inversion_personal": scores[7],
				"comprension_mutua": scores[8],
				"diversion_compartida": scores[9]
			}
			gen = parts[11].upper().strip()
			if gen == "H":  # convertir "H" a "M"
				gen = "M"
			categoria = parts[12]
		elif len(parts) == 12:
			nombre = parts[0]
			scores = list(map(int, parts[1:11]))
			puntuaciones = {
				"tiempo_compartido": scores[0],
				"apoyo_emocional": scores[1],
				"intereses_comunes": scores[2],
				"frecuencia_comunicacion": scores[3],
				"confianza": scores[4],
				"reciprocidad": scores[5],
				"resolucion_conflictos": scores[6],
				"inversion_personal": scores[7],
				"comprension_mutua": scores[8],
				"diversion_compartida": scores[9]
			}
			# El campo 11 contiene género seguido de la categoría, ej. "MTerciario"
			campo = parts[11].strip()
			if campo:
				gen = campo[0].upper()
				if gen == "H":
					gen = "M"
				categoria = campo[1:].strip() if len(campo) > 1 else "Desconocido"
			else:
				gen = "M"
				categoria = "Desconocido"
		else:
			raise ValueError("La línea no contiene suficientes datos para un amigo.")
		amigo = Amigo(nombre, puntuaciones, gen, categoria)
		amigo.clasificar_amigo()
		return amigo
