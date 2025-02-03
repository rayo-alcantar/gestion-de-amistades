# main.py

import wx
from circulo_amistad import CirculoAmistad
from amigo_dialog import AmigoDialog
from reevaluar_amigo_dialog import ReevaluarAmigoDialog
from eliminar_amigo_dialog import EliminarAmigoDialog

class AmigosApp(wx.Frame):
	def __init__(self, parent, title="Gestión de Amistades"):
		super(AmigosApp, self).__init__(parent, title=title, size=(500, 400))
		self.circulo = CirculoAmistad()
		self.InitUI()
	
	def InitUI(self):
		panel = wx.Panel(self)  # No se incluye el filtro en la principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Botón para agregar un nuevo amigo (con atajo)
		add_btn = wx.Button(panel, label="&Agregar Amigo")
		add_btn.Bind(wx.EVT_BUTTON, self.on_add_amigo)
		sizer.Add(add_btn, 0, wx.ALL | wx.EXPAND, 5)
		
		# Botón para reevaluar/editar un amigo (con atajo)
		eval_btn = wx.Button(panel, label="&Reevaluar/Editar Amigo")
		eval_btn.Bind(wx.EVT_BUTTON, self.on_reevaluar_amigo)
		sizer.Add(eval_btn, 0, wx.ALL | wx.EXPAND, 5)
		
		# Botón para eliminar un amigo (con atajo)
		del_btn = wx.Button(panel, label="&Eliminar Amigo")
		del_btn.Bind(wx.EVT_BUTTON, self.on_eliminar_amigo)
		sizer.Add(del_btn, 0, wx.ALL | wx.EXPAND, 5)
		
		# Botón para mostrar la lista de amigos (con atajo)
		show_btn = wx.Button(panel, label="&Mostrar Amigos")
		show_btn.Bind(wx.EVT_BUTTON, self.on_mostrar_amigos)
		sizer.Add(show_btn, 0, wx.ALL | wx.EXPAND, 5)
		
		# Botón para salir de la aplicación (con atajo)
		exit_btn = wx.Button(panel, label="&Salir")
		exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
		sizer.Add(exit_btn, 0, wx.ALL | wx.EXPAND, 5)
		
		panel.SetSizer(sizer)
		self.Centre()
	
	def on_add_amigo(self, event):
		dialog = AmigoDialog(self, title="Agregar Amigo")
		if dialog.ShowModal() == wx.ID_OK:
			nombre, puntuaciones, genero = dialog.obtener_datos()
			self.circulo.agregar_amigo(nombre, puntuaciones, genero)
			wx.MessageBox("Amigo añadido correctamente.", "Información", wx.OK | wx.ICON_INFORMATION)
		dialog.Destroy()
	
	def on_reevaluar_amigo(self, event):
		dialog = ReevaluarAmigoDialog(self, circulo=self.circulo, title="Reevaluar/Editar Amigo")
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
		# Se crea un diálogo exclusivo para mostrar amigos con filtro incluido
		filtro_options = [
			"Todos", "Hombres", "Mujeres",
			"Súper Amigo", "Primario", "Secundario", "Terciario", "Ocasional", "Conocido",
			"Puntuación ≥ 80"
		]
		dialog = wx.Dialog(self, title="Lista de Amigos", size=(400, 450), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
		panel = wx.Panel(dialog, style=wx.TAB_TRAVERSAL)
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Filtro (combo box) dentro del diálogo
		filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
		filter_label = wx.StaticText(panel, label="Filtrar:")
		filter_sizer.Add(filter_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
		filtro_choice = wx.Choice(panel, choices=filtro_options)
		filtro_choice.SetSelection(0)
		filter_sizer.Add(filtro_choice, 0, wx.ALL, 5)
		sizer.Add(filter_sizer, 0, wx.EXPAND | wx.ALL, 5)
		
		# Área de texto para mostrar la lista
		text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
		
		# Botón para cerrar el diálogo
		close_btn = wx.Button(panel, label="&Cerrar")
		sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 5)
		
		panel.SetSizer(sizer)
		
		# Función para actualizar el listado según el filtro seleccionado
		def update_list(event=None):
			filtro = filtro_choice.GetStringSelection()
			# Ordenar amigos de mayor a menor según la suma de las puntuaciones
			amigos_ordenados = sorted(self.circulo.amigos, key=lambda a: sum(a.puntuaciones.values()), reverse=True)
			amigos_info = []
			count = 0
			for amigo in amigos_ordenados:
				genero_text = "Hombre" if amigo.genero == "M" else "Mujer"
				# Aplicar filtro según la opción seleccionada
				if filtro == "Hombres" and genero_text != "Hombre":
					continue
				if filtro == "Mujeres" and genero_text != "Mujer":
					continue
				if filtro in ["Súper Amigo", "Primario", "Secundario", "Terciario", "Ocasional", "Conocido"]:
					if amigo.categoria != filtro:
						continue
				if filtro == "Puntuación ≥ 80":
					if sum(amigo.puntuaciones.values()) < 80:
						continue
				count += 1
				# Mostrar información: el género se muestra solo como "Hombre" o "Mujer"
				amigos_info.append(f"{amigo.nombre}, Puntuación Total: {sum(amigo.puntuaciones.values())}, "
									 f"Categoría: {amigo.categoria}, {genero_text}")
			encabezado = f"Mostrando {count} amigos (Filtro: {filtro})"
			info_str = encabezado + "\n" + "\n".join(amigos_info)
			text_ctrl.SetValue(info_str)
		
		filtro_choice.Bind(wx.EVT_CHOICE, update_list)
		update_list()  # Inicializar listado
		
		close_btn.Bind(wx.EVT_BUTTON, lambda event: dialog.EndModal(wx.ID_OK))
		
		dialog.ShowModal()
		dialog.Destroy()
	
	def on_exit(self, event):
		self.Close(True)

def main():
	app = wx.App()
	frame = AmigosApp(None, title="Gestión de Amistades")
	frame.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
