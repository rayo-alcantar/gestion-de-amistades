# amigo_dialog.py

import wx

class AmigoDialog(wx.Dialog):
	def __init__(self, parent, title="Agregar Amigo"):
		super(AmigoDialog, self).__init__(parent, title=title, size=(300, 500))
		
		self.panel = wx.Panel(self)
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Campo para ingresar el nombre del amigo
		wx.StaticText(self.panel, label="Nombre del Amigo:")
		self.nombre_ctrl = wx.TextCtrl(self.panel)
		self.main_sizer.Add(self.nombre_ctrl, 0, wx.EXPAND | wx.ALL, 5)
		
		# Cuadro combinado para seleccionar el género
		wx.StaticText(self.panel, label="Género:")
		self.genero_choice = wx.Choice(self.panel, choices=["Hombre", "Mujer"])
		self.genero_choice.SetSelection(0)  # Por defecto "Hombre"
		self.main_sizer.Add(self.genero_choice, 0, wx.EXPAND | wx.ALL, 5)
		
		# Diccionario para almacenar los TextCtrls de las puntuaciones
		self.puntuaciones_ctrls = {}
		self.lista_puntuaciones = [
			"tiempo_compartido", "apoyo_emocional", "intereses_comunes",
			"frecuencia_comunicacion", "confianza", "reciprocidad", 
			"resolucion_conflictos", "inversion_personal", "comprension_mutua", 
			"diversion_compartida"
		]
		
		for puntuacion in self.lista_puntuaciones:
			wx.StaticText(self.panel, label=puntuacion.replace("_", " ").title() + ":")
			ctrl = wx.TextCtrl(self.panel)
			self.puntuaciones_ctrls[puntuacion] = ctrl
			self.main_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
		
		# Botón para aceptar y validar las entradas (con atajo)
		ok_button = wx.Button(self.panel, label="&Aceptar")
		ok_button.Bind(wx.EVT_BUTTON, self.on_accept)
		self.main_sizer.Add(ok_button, 0, wx.EXPAND | wx.ALL, 5)
		
		self.panel.SetSizer(self.main_sizer)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
	
	def on_key(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_CANCEL)
		else:
			event.Skip()
	
	def on_accept(self, event):
		try:
			if not self.nombre_ctrl.GetValue().strip():
				raise ValueError("El nombre no puede estar vacío.")
			if self.genero_choice.GetSelection() == wx.NOT_FOUND:
				raise ValueError("Debe seleccionar un género.")
			puntuaciones = {key: int(ctrl.GetValue()) for key, ctrl in self.puntuaciones_ctrls.items()}
			if not all(1 <= p <= 10 for p in puntuaciones.values()):
				raise ValueError("Las puntuaciones deben estar entre 1 y 10.")
			self.EndModal(wx.ID_OK)
		except ValueError as e:
			wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
	
	def obtener_datos(self):
		nombre = self.nombre_ctrl.GetValue().strip()
		genero_text = self.genero_choice.GetStringSelection()
		genero = "M" if genero_text == "Hombre" else "F"
		puntuaciones = {key: int(ctrl.GetValue()) for key, ctrl in self.puntuaciones_ctrls.items()}
		return nombre, puntuaciones, genero
