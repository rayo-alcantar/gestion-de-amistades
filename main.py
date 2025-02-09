# main.py
# encoding: utf-8
import wx
import os
from circulo_amistad import CirculoAmistad
from amigo_dialog import AmigoDialog
from reevaluar_amigo_dialog import ReevaluarAmigoDialog
from eliminar_amigo_dialog import EliminarAmigoDialog

def cargar_criterios(nombre_archivo="criterios.txt"):
	"""
	Carga los criterios desde un archivo de texto.
	Si el archivo no existe, se crea uno con ejemplos y se muestra un mensaje en la GUI
	para que el usuario lo edite con sus propios criterios.
	Se espera que el archivo contenga exactamente 10 criterios, uno por línea.
	Si no tiene 10, se muestra un mensaje y se utilizan criterios de ejemplo por defecto.
	"""
	criterios_de_ejemplo = [
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

	# Si el archivo no existe, crearlo con criterios de ejemplo.
	if not os.path.exists(nombre_archivo):
		with open(nombre_archivo, 'w', encoding='utf-8') as f:
			for linea in criterios_de_ejemplo:
				f.write(linea + "\n")
		# Se retorna la lista de ejemplo y se mostrará un mensaje más adelante, 
		# una vez que la app wx esté disponible.
		return criterios_de_ejemplo, True

	# Si el archivo existe, leerlo.
	with open(nombre_archivo, 'r', encoding='utf-8') as f:
		criterios = [linea.strip() for linea in f if linea.strip()]

	# Si la cantidad de criterios no es 10, usar los criterios de ejemplo.
	if len(criterios) != 10:
		return criterios_de_ejemplo, True

	# Caso en que todo está correcto.
	return criterios, False


class AmigosApp(wx.Frame):
	"""
	Clase principal de la aplicación de gestión de amistades.
	Permite agregar, reevaluar/editar, eliminar y mostrar amigos del círculo de amistades.
	"""
	def __init__(self, parent, title="Gestión de Amistades", criterios=None):
		super(AmigosApp, self).__init__(parent, title=title, size=(500, 400))
		self.criterios = criterios
		self.circulo = CirculoAmistad(criterios=self.criterios)
		self.InitUI()

	def InitUI(self):
		# Se crea el panel principal y se organiza con un sizer vertical.
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Botón para agregar un nuevo amigo.
		add_btn = wx.Button(panel, label="&Agregar Amigo")
		add_btn.Bind(wx.EVT_BUTTON, self.on_add_amigo)
		sizer.Add(add_btn, 0, wx.ALL | wx.EXPAND, 5)

		# Botón para reevaluar/editar un amigo.
		eval_btn = wx.Button(panel, label="&Reevaluar/Editar Amigo")
		eval_btn.Bind(wx.EVT_BUTTON, self.on_reevaluar_amigo)
		sizer.Add(eval_btn, 0, wx.ALL | wx.EXPAND, 5)

		# Botón para eliminar un amigo.
		del_btn = wx.Button(panel, label="&Eliminar Amigo")
		del_btn.Bind(wx.EVT_BUTTON, self.on_eliminar_amigo)
		sizer.Add(del_btn, 0, wx.ALL | wx.EXPAND, 5)

		# Botón para mostrar la lista de amigos.
		show_btn = wx.Button(panel, label="&Mostrar Amigos")
		show_btn.Bind(wx.EVT_BUTTON, self.on_mostrar_amigos)
		sizer.Add(show_btn, 0, wx.ALL | wx.EXPAND, 5)

		# Botón para salir de la aplicación.
		exit_btn = wx.Button(panel, label="&Salir")
		exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
		sizer.Add(exit_btn, 0, wx.ALL | wx.EXPAND, 5)

		panel.SetSizer(sizer)
		self.Centre()

	def on_add_amigo(self, event):
		dialog = AmigoDialog(self, title="Agregar Amigo", criterios=self.criterios)
		if dialog.ShowModal() == wx.ID_OK:
			nombre, puntuaciones, genero = dialog.obtener_datos()
			self.circulo.agregar_amigo(nombre, puntuaciones, genero)
			wx.MessageBox("Amigo añadido correctamente.", "Información", wx.OK | wx.ICON_INFORMATION)
		dialog.Destroy()

	def on_reevaluar_amigo(self, event):
		dialog = ReevaluarAmigoDialog(self, circulo=self.circulo, title="Reevaluar/Editar Amigo", criterios=self.criterios)
		dialog.ShowModal()
		dialog.Destroy()

	def on_eliminar_amigo(self, event):
		dialog = EliminarAmigoDialog(self, circulo=self.circulo, title="Eliminar Amigo")
		if dialog.ShowModal() == wx.ID_OK:
			indice = dialog.obtener_indice_seleccionado()
			if self.circulo.eliminar_amigo(indice):
				wx.MessageBox("Amigo eliminado correctamente.", "Información", wx.OK | wx.ICON_INFORMATION)
			else:
				wx.MessageBox("Error al eliminar el amigo.", "Error", wx.OK | wx.ICON_ERROR)
		dialog.Destroy()

	def on_mostrar_amigos(self, event):
		"""
		Muestra la lista de amigos en un diálogo con opción de filtrado.
		Se han realizado las siguientes modificaciones:
		  - Se ha eliminado el filtro de 'Puntuación ≥ 80'.
		  - Se muestra, en el encabezado, el porcentaje de amigos filtrados respecto al total.
		"""
		# Opciones de filtro disponibles (se elimina la opción de 'Puntuación ≥ 80')
		filtro_options = [
			"Todos", "Hombres", "Mujeres",
			"Súper Amigo", "Primario", "Secundario", "Terciario", "Ocasional", "Conocido"
		]

		# Crear el diálogo para mostrar la lista de amigos.
		dialog = wx.Dialog(self, title="Lista de Amigos", size=(400, 450),
						   style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
		panel = wx.Panel(dialog, style=wx.TAB_TRAVERSAL)
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Sección del filtro: etiqueta y combo box.
		filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
		filter_label = wx.StaticText(panel, label="Filtrar:")
		filter_sizer.Add(filter_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
		filtro_choice = wx.Choice(panel, choices=filtro_options)
		filtro_choice.SetSelection(0)  # Selección por defecto: "Todos"
		filter_sizer.Add(filtro_choice, 0, wx.ALL, 5)
		sizer.Add(filter_sizer, 0, wx.EXPAND | wx.ALL, 5)

		# Área de texto para mostrar la información de los amigos.
		text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

		# Botón para cerrar el diálogo.
		close_btn = wx.Button(panel, label="&Cerrar")
		sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 5)

		panel.SetSizer(sizer)

		def update_list(event=None):
			"""
			Actualiza la lista de amigos según el filtro seleccionado.
			Se ordenan los amigos de mayor a menor por la suma de sus puntuaciones.
			Se aplica el filtro elegido y se calcula el porcentaje de amigos filtrados
			respecto al total, mostrando dicha información en el encabezado.
			"""
			# Obtener la opción de filtro seleccionada.
			filtro = filtro_choice.GetStringSelection()

			# Ordenar los amigos de mayor a menor según la suma de sus puntuaciones.
			amigos_ordenados = sorted(
				self.circulo.amigos,
				key=lambda a: sum(a.puntuaciones.values()),
				reverse=True
			)
			amigos_info = []  # Lista para almacenar la información de cada amigo.
			count = 0		 # Contador de amigos que cumplen con el filtro.

			# Recorrer cada amigo en la lista ordenada.
			for amigo in amigos_ordenados:
				# Convertir el valor del género a un texto legible.
				genero_text = "Hombre" if amigo.genero == "M" else "Mujer"

				# Filtrar por género.
				if filtro == "Hombres" and genero_text != "Hombre":
					continue
				if filtro == "Mujeres" and genero_text != "Mujer":
					continue

				# Filtrar por categoría de amistad.
				if filtro in ["Súper Amigo", "Primario", "Secundario", "Terciario", "Ocasional", "Conocido"]:
					if amigo.categoria != filtro:
						continue

				# Si pasa los filtros, se incrementa el contador y se guarda la información.
				count += 1
				amigos_info.append(
					f"{amigo.nombre}, Puntuación Total: {sum(amigo.puntuaciones.values())}, "
					f"Categoría: {amigo.categoria}, {genero_text}"
				)

			# Calcular el porcentaje de amigos filtrados respecto al total del círculo.
			total_amigos = len(self.circulo.amigos)
			porcentaje = (count / total_amigos * 100) if total_amigos > 0 else 0

			# Encabezado que muestra la cantidad de amigos filtrados y el porcentaje calculado.
			encabezado = f"Mostrando lista de {count} amigos (Filtro: {filtro}) - {porcentaje:.1f}% del total"
			info_str = encabezado + "\n" + "\n".join(amigos_info)
			text_ctrl.SetValue(info_str)

		# Vincular el evento de cambio en el filtro a la función de actualización.
		filtro_choice.Bind(wx.EVT_CHOICE, update_list)
		update_list()  # Inicializar la lista con el filtro por defecto.

		# Vincular el botón de cierre para terminar el diálogo.
		close_btn.Bind(wx.EVT_BUTTON, lambda event: dialog.EndModal(wx.ID_OK))

		dialog.ShowModal()
		dialog.Destroy()

	def on_exit(self, event):
		self.Close(True)


def main():
	# Se inicializa la aplicación de wxPython primero para poder mostrar mensajes con wx.MessageBox.
	app = wx.App()
	# Verificar si ya hay una instancia ejecutándose
	name = "manage-friends-Instance"  # Identificador para la aplicación
	instance = wx.SingleInstanceChecker(name)
	if instance.IsAnotherRunning():
		wx.MessageBox("el gestor de amistades ya está en ejecución.", "Aviso", wx.ICON_INFORMATION)
		return False


	criterios, hubo_problema = cargar_criterios()

	# Si hubo_problema es True, se muestra un mensaje en la GUI indicando la acción tomada.
	if hubo_problema:
		wx.MessageBox(
			"Se han creado o ajustado criterios de ejemplo porque el archivo no existía "
			"o no contenía exactamente 10 líneas. Por favor, revise el archivo 'criterios.txt'.",
			"Información",
			wx.OK | wx.ICON_INFORMATION
		)

	frame = AmigosApp(None, title="Gestión de Amistades", criterios=criterios)
	frame.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()
