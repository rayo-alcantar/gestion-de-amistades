# amigo.py
import csv
import io
from typing import Dict, List, Optional, Union

class Amigo:
    def __init__(self, nombre: str, puntuaciones: Optional[Dict[str, int]] = None, genero: str = "M", categoria: Optional[str] = None, criterios: Optional[List[str]] = None):
        """
        Inicializa un objeto Amigo.
        
        :param nombre: Nombre del amigo.
        :param puntuaciones: Diccionario con puntuaciones; si no se proporciona, se inicializa con 0 para cada pregunta.
        :param genero: 'M' para Hombre o 'F' para Mujer. Por defecto es 'M'.
        :param categoria: Categoría del amigo; si no se especifica se asigna "Desconocido".
        :param criterios: Lista de criterios (criterios) para la evaluación.
        """
        self.nombre = nombre.strip()
        if criterios is None:
            # Valor por defecto en caso de no recibir la lista de criterios
            self.criterios = [
                "Empatía y Calidez",
                "Confianza",
                "Reciprocidad",
                "Intereses Compartidos",
                "Disponibilidad y Presencia",
                "Comunicación Efectiva",
                "Apoyo en Dificultades",
                "Resolución de Conflictos",
                "Diversión y Recreación",
                "Crecimiento Personal"
            ]
        else:
            self.criterios = criterios
        
        if puntuaciones is None:
            self.puntuaciones = { key: 0 for key in self.criterios }
        else:
            self.puntuaciones = puntuaciones
        
        # Normalizar: si se recibe "H" se trata como "M"
        gen = genero.upper().strip()
        if gen == "H":
            gen = "M"
        self.genero = gen if gen in ("M", "F") else "M"
        self.categoria = categoria or "Desconocido"
        self.clasificar_amigo()

    def actualizar_puntuaciones(self, nuevas_puntuaciones: Dict[str, int]):
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

    def editar_nombre(self, nuevo_nombre: str):
        """Permite editar el nombre del amigo."""
        self.nombre = nuevo_nombre.strip()

    def editar_genero(self, nuevo_genero: str):
        """Permite editar el género del amigo.
        
        Se espera que nuevo_genero sea 'M' o 'F'. Si se pasa otro valor, se asigna 'M' por defecto.
        """
        nuevo_genero = nuevo_genero.upper().strip()
        if nuevo_genero not in ("M", "F"):
            nuevo_genero = "M"
        self.genero = nuevo_genero

    def __str__(self) -> str:
        detalles = f"Nombre: {self.nombre}\n"
        detalles += f"Género: {'Hombre' if self.genero == 'M' else 'Mujer'}\n"
        for pregunta in self.criterios:
            detalles += f"{pregunta}: {self.puntuaciones.get(pregunta, 0)}\n"
        detalles += f"Categoría: {self.categoria}\n"
        return detalles

    def to_line(self) -> str:
        """
        Convierte la información del amigo en una línea CSV.
        Formato: Nombre, score1, score2, ..., score10, Género, Categoría
        """
        output = io.StringIO()
        writer = csv.writer(output)
        row = [self.nombre] + [self.puntuaciones.get(q, 0) for q in self.criterios] + [self.genero, self.categoria]
        writer.writerow(row)
        return output.getvalue().strip()

    @classmethod
    def from_line(cls, line: str, criterios: List[str]) -> 'Amigo':
        """
        Crea un objeto Amigo a partir de una línea CSV.
        """
        # Usar csv.reader para manejar correctamente comillas y comas en nombres
        reader = csv.reader([line.strip()])
        try:
            parts = next(reader)
        except StopIteration:
            raise ValueError("Línea vacía")
        
        num_preg = len(criterios)
        
        # Validar longitud mínima
        if len(parts) < num_preg + 2:
             raise ValueError("La línea no contiene suficientes datos para un amigo.")

        nombre = parts[0]
        
        # Intentar parsear scores
        try:
            scores = list(map(int, parts[1:num_preg+1]))
        except ValueError:
             raise ValueError("Error al parsear puntuaciones.")
             
        puntuaciones = { criterios[i]: scores[i] for i in range(num_preg) }
        
        # Manejo flexible de género y categoría para retrocompatibilidad
        # Formato ideal: [nombre, scores..., genero, categoria]
        if len(parts) >= num_preg + 3:
            gen = parts[num_preg+1].upper().strip()
            categoria = parts[num_preg+2]
        else:
            # Formato antiguo o compacto: el último campo contiene genero y categoría
            campo = parts[num_preg+1].strip()
            if campo:
                gen = campo[0].upper()
                categoria = campo[1:].strip() if len(campo) > 1 else "Desconocido"
            else:
                gen = "M"
                categoria = "Desconocido"
        
        if gen == "H":
            gen = "M"
            
        amigo = cls(nombre, puntuaciones, gen, categoria, criterios=criterios)
        amigo.clasificar_amigo()
        return amigo
