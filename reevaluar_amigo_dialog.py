# reevaluar_amigo_dialog.py

import wx

class ReevaluarAmigoDialog(wx.Dialog):
	def __init__(self, parent, circulo, title="Reevaluar Amigo", criterios=None):
		super(ReevaluarAmigoDialog, self).__init__(parent, title=title, size=(350, 600))
		
		self.circulo = circulo
		self.criterios = criterios
		self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Combo para filtrar la lista de amigos por género
		filtro_sizer = wx.BoxSizer(wx.HORIZONTAL)
		filtro_label = wx.StaticText(self.panel, label="Filtrar por:")
		filtro_sizer.Add(filtro_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
		self.filtro_choice = wx.Choice(self.panel, choices=["Todos", "Hombres", "Mujeres"])
		self.filtro_choice.SetSelection(0)
		self.filtro_choice.Bind(wx.EVT_CHOICE, self.on_filter_changed)
		filtro_sizer.Add(self.filtro_choice, 0, wx.ALL, 5)
		self.main_sizer.Add(filtro_sizer, 0, wx.EXPAND)
		
		# Combo para seleccionar el amigo (actualizable según el filtro)
		wx.StaticText(self.panel, label="Seleccione un Amigo:")
		self.amigo_choice = wx.Choice(self.panel, choices=[])
		self.amigo_choice.Bind(wx.EVT_CHOICE, self.on_select_amigo)
		self.main_sizer.Add(self.amigo_choice, 0, wx.EXPAND | wx.ALL, 5)
		
		# Área para mostrar detalle (toString) claro del amigo seleccionado
		wx.StaticText(self.panel, label="Detalle del Amigo:")
		self.detail_text = wx.StaticText(self.panel, label="")
		self.main_sizer.Add(self.detail_text, 0, wx.EXPAND | wx.ALL, 5)
		
		# Campo para editar el nombre
		wx.StaticText(self.panel, label="Editar Nombre:")
		self.nombre_ctrl = wx.TextCtrl(self.panel)
		self.main_sizer.Add(self.nombre_ctrl, 0, wx.EXPAND | wx.ALL, 5)
		
		# Combo para editar el género
		wx.StaticText(self.panel, label="Género:")
		self.genero_choice = wx.Choice(self.panel, choices=["Hombre", "Mujer"])
		self.main_sizer.Add(self.genero_choice, 0, wx.EXPAND | wx.ALL, 5)
		
		# Campos para las 10 puntuaciones utilizando las criterios proporcionadas
		self.puntuaciones_ctrls = {}
		if criterios is None:
			self.lista_puntuaciones = []
		else:
			self.lista_puntuaciones = criterios
		for clave in self.lista_puntuaciones:
			wx.StaticText(self.panel, label=clave + ":")
			ctrl = wx.SpinCtrl(self.panel, value="0", min=0, max=10)
			self.puntuaciones_ctrls[clave] = ctrl
			self.main_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
		
		# Botones: Actualizar y Cancelar
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		update_btn = wx.Button(self.panel, label="&Actualizar")
		update_btn.Bind(wx.EVT_BUTTON, self.on_update)
		btn_sizer.Add(update_btn, 0, wx.ALL, 5)
		cancel_btn = wx.Button(self.panel, label="&Cancelar")
		cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
		self.main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
		
		self.panel.SetSizer(self.main_sizer)
		
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		
		# Inicializar la lista de amigos según el filtro (por defecto "Todos")
		self.reload_friends()
		if self.amigo_choice.GetCount() > 0:
			self.amigo_choice.SetSelection(0)
			self.on_select_amigo(None)
		
		self.original_nombre = ""
		self.original_genero = ""
		self.original_puntuaciones = {}
	
	def on_key(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.on_cancel(None)
		else:
			event.Skip()
	
	def on_close(self, event):
		self.on_cancel(None)
	
	def on_filter_changed(self, event):
		self.reload_friends()
		if self.amigo_choice.GetCount() > 0:
			self.amigo_choice.SetSelection(0)
			self.on_select_amigo(None)
	
	def reload_friends(self):
		"""Filtra y ordena la lista de amigos (de mayor a menor puntuación) según el filtro seleccionado."""
		filtro = self.filtro_choice.GetStringSelection()
		todos = sorted(self.circulo.amigos, key=lambda a: sum(a.puntuaciones.values()), reverse=True)
		if filtro == "Todos":
			self.friends_sorted = todos
		elif filtro == "Hombres":
			self.friends_sorted = [a for a in todos if a.genero == "M"]
		else:
			self.friends_sorted = [a for a in todos if a.genero == "F"]
		self.amigo_choice.Clear()
		self.amigo_choice.AppendItems([a.nombre for a in self.friends_sorted])
	
	def on_select_amigo(self, event):
		idx = self.amigo_choice.GetSelection()
		if idx == wx.NOT_FOUND:
			return
		amigo = self.friends_sorted[idx]
		self.nombre_ctrl.SetValue(amigo.nombre)
		self.detail_text.SetLabel(self.formatear_detalle(amigo))
		if amigo.genero == "M":
			self.genero_choice.SetSelection(0)
		else:
			self.genero_choice.SetSelection(1)
		for clave, ctrl in self.puntuaciones_ctrls.items():
			ctrl.SetValue(str(amigo.puntuaciones.get(clave, 0)))
		self.original_nombre = amigo.nombre
		self.original_genero = amigo.genero
		self.original_puntuaciones = { k: str(amigo.puntuaciones.get(k, 0)) for k in self.lista_puntuaciones }
	
	def formatear_detalle(self, amigo):
		"""Devuelve un string formateado con detalles claros del amigo."""
		detalle = f"Nombre: {amigo.nombre}\n"
		detalle += f"Género: {'Hombre' if amigo.genero=='M' else 'Mujer'}\n"
		detalle += "Puntuaciones:\n"
		for clave in self.lista_puntuaciones:
			detalle += f"  {clave}: {amigo.puntuaciones.get(clave,0)}\n"
		detalle += f"Categoría: {amigo.categoria}"
		return detalle
	
	def has_unsaved_changes(self):
		if self.nombre_ctrl.GetValue().strip() != self.original_nombre:
			return True
		cur_gen = "M" if self.genero_choice.GetStringSelection() == "Hombre" else "F"
		if cur_gen != self.original_genero:
			return True
		for clave, ctrl in self.puntuaciones_ctrls.items():
			if ctrl.GetValue() != self.original_puntuaciones.get(clave, ""):
				return True
		return False
	
	def on_update(self, event):
		try:
			idx = self.amigo_choice.GetSelection()
			if idx == wx.NOT_FOUND:
				raise ValueError("Debe seleccionar un amigo.")
			nuevo_nombre = self.nombre_ctrl.GetValue().strip()
			if not nuevo_nombre:
				raise ValueError("El nombre no puede estar vacío.")
			gen_text = self.genero_choice.GetStringSelection()
			nuevo_gen = "M" if gen_text == "Hombre" else "F"
			nuevas_puntuaciones = {}
			for clave, ctrl in self.puntuaciones_ctrls.items():
				try:
					valor  =ctrl.GetValue()
				except ValueError:
					raise ValueError(f"El valor de '{clave}' debe ser un número entero.")
				nuevas_puntuaciones[clave] = valor
			if not all(1 <= p <= 10 for p in nuevas_puntuaciones.values()):
				raise ValueError("Las puntuaciones deben estar entre 1 y 10.")
			amigo_actual = self.friends_sorted[idx]
			amigo_actual.editar_nombre(nuevo_nombre)
			amigo_actual.actualizar_puntuaciones(nuevas_puntuaciones)
			amigo_actual.editar_genero(nuevo_gen)
			self.circulo.guardar_amigos()
			detalle = "Amigo actualizado:\n" + self.formatear_detalle(amigo_actual)
			wx.MessageBox(detalle, "Información", wx.OK | wx.ICON_INFORMATION)
			self.reload_friends()
			nuevo_idx = 0
			for i, a in enumerate(self.friends_sorted):
				if a.nombre == amigo_actual.nombre:
					nuevo_idx = i
					break
			self.amigo_choice.SetSelection(nuevo_idx)
			self.on_select_amigo(None)
			self.amigo_choice.SetFocus()
		except ValueError as e:
			wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
	
	def on_cancel(self, event):
		if self.has_unsaved_changes():
			dlg = wx.MessageDialog(self,
								   "Existen cambios sin guardar. ¿Desea salir sin guardar?",
								   "Confirmar",
								   wx.YES_NO | wx.ICON_WARNING)
			if dlg.ShowModal() == wx.ID_NO:
				dlg.Destroy()
				return
			dlg.Destroy()
		self.Destroy()
	
	def obtener_datos(self):
		return None
