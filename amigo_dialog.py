# amigo_dialog.py

import wx

class AmigoDialog(wx.Dialog):
	def __init__(self, parent, title="Agregar Amigo"):
		super(AmigoDialog, self).__init__(parent, title=title, size=(300, 550))
		
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
		# Se usan 10 criterios nuevos
		self.puntuaciones_ctrls = {}
		self.lista_puntuaciones = [
			"empatia_calidez",		 # Mide la capacidad para ponerse en tu lugar y transmitir calidez
			"confianza",			   # Evalúa cuán confiable es la persona para compartir aspectos personales
			"reciprocidad",			# Mide el equilibrio en el dar y recibir apoyo
			"intereses_compartidos",   # Evalúa la coincidencia en hobbies, valores o actividades
			"disponibilidad_presencia",# Considera la facilidad de contar con su presencia
			"comunicacion_efectiva",   # Mide la claridad y calidad de la comunicación
			"apoyo_dificultades",	  # Evalúa el soporte brindado en momentos críticos
			"resolucion_conflictos",   # Mide la capacidad para resolver desacuerdos de forma constructiva
			"diversion_recreacion",	# Evalúa si la amistad genera momentos divertidos y de esparcimiento
			"crecimiento_personal"	 # Mide si la relación inspira o fomenta el desarrollo personal
		]
		
		for criterio in self.lista_puntuaciones:
			# Crear una etiqueta más amigable: convertir "_" en espacios y formatear en Title Case
			label = criterio.replace("_", " ").title()
			wx.StaticText(self.panel, label=label + ":")
			ctrl = wx.TextCtrl(self.panel)
			self.puntuaciones_ctrls[criterio] = ctrl
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
			# Convertir los valores de los campos de puntuaciones a enteros
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
