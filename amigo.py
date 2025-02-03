# amigo.py

class Amigo:
	def __init__(self, nombre, puntuaciones=None, genero="M", categoria=None):
		"""
		:param nombre: Nombre del amigo.
		:param puntuaciones: Diccionario con 10 puntuaciones; si no se proporciona se inicializa en 0.
		:param genero: 'M' para Hombre o 'F' para Mujer. Por defecto es 'M'.
		:param categoria: Categoría del amigo; si no se especifica se asigna "Desconocido".
		"""
		self.nombre = nombre.strip()
		# Usamos los 10 criterios alternativos
		self.puntuaciones = puntuaciones if puntuaciones else {
			"empatia_calidez": 0,
			"confianza": 0,
			"reciprocidad": 0,
			"intereses_compartidos": 0,
			"disponibilidad_presencia": 0,
			"comunicacion_efectiva": 0,
			"apoyo_dificultades": 0,
			"resolucion_conflictos": 0,
			"diversion_recreacion": 0,
			"crecimiento_personal": 0
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
		"""Clasifica al amigo en una categoría basada en la suma total de sus puntuaciones."""
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
		# Presenta cada criterio con una etiqueta clara
		for clave, valor in self.puntuaciones.items():
			# Se reemplazan guiones bajos por espacios y se capitaliza
			detalles += f"{clave.replace('_',' ').title()}: {valor}\n"
		detalles += f"Categoría: {self.categoria}\n"
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
		 - 12 campos: [nombre, 10 puntuaciones, género+categoría],
		   en cuyo caso se toma el primer carácter como género (con "H" convertido a "M")
		   y el resto como categoría.
		"""
		parts = line.strip().split(',')
		if len(parts) == 13:
			nombre = parts[0]
			scores = list(map(int, parts[1:11]))
			puntuaciones = {
				"empatia_calidez": scores[0],
				"confianza": scores[1],
				"reciprocidad": scores[2],
				"intereses_compartidos": scores[3],
				"disponibilidad_presencia": scores[4],
				"comunicacion_efectiva": scores[5],
				"apoyo_dificultades": scores[6],
				"resolucion_conflictos": scores[7],
				"diversion_recreacion": scores[8],
				"crecimiento_personal": scores[9]
			}
			gen = parts[11].upper().strip()
			if gen == "H":
				gen = "M"
			categoria = parts[12]
		elif len(parts) == 12:
			nombre = parts[0]
			scores = list(map(int, parts[1:11]))
			puntuaciones = {
				"empatia_calidez": scores[0],
				"confianza": scores[1],
				"reciprocidad": scores[2],
				"intereses_compartidos": scores[3],
				"disponibilidad_presencia": scores[4],
				"comunicacion_efectiva": scores[5],
				"apoyo_dificultades": scores[6],
				"resolucion_conflictos": scores[7],
				"diversion_recreacion": scores[8],
				"crecimiento_personal": scores[9]
			}
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
