import wx

class ReevaluarAmigoDialog(wx.Dialog):
	def __init__(self, parent, circulo, title="Reevaluar Amigo"):
		super(ReevaluarAmigoDialog, self).__init__(parent, title=title, size=(350, 600))
		
		self.circulo = circulo
		# Usamos TAB_TRAVERSAL para que todos los controles sean accesibles con Tab.
		self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Combo para filtrar amigos por género
		filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
		filter_label = wx.StaticText(self.panel, label="Filtrar por género:")
		filter_sizer.Add(filter_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
		self.filtro_choice = wx.Choice(self.panel, choices=["Todos", "Hombres", "Mujeres"])
		self.filtro_choice.SetSelection(0)
		self.filtro_choice.Bind(wx.EVT_CHOICE, self.on_filter_changed)
		filter_sizer.Add(self.filtro_choice, 0, wx.ALL, 5)
		self.main_sizer.Add(filter_sizer, 0, wx.EXPAND)
		
		# Combo para seleccionar el amigo (se actualizará según el filtro)
		wx.StaticText(self.panel, label="Seleccione un Amigo:")
		self.amigo_choice = wx.Choice(self.panel, choices=[])
		self.amigo_choice.Bind(wx.EVT_CHOICE, self.on_select_amigo)
		self.main_sizer.Add(self.amigo_choice, 0, wx.EXPAND | wx.ALL, 5)
		
		# Área para mostrar los detalles (toString) del amigo seleccionado
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
		
		# Campos para las puntuaciones
		self.puntuaciones_ctrls = {}
		self.lista_puntuaciones = [
			"tiempo_compartido", "apoyo_emocional", "intereses_comunes",
			"frecuencia_comunicacion", "confianza", "reciprocidad", 
			"resolucion_conflictos", "inversion_personal", "comprension_mutua", 
			"diversion_compartida"
		]
		for p in self.lista_puntuaciones:
			wx.StaticText(self.panel, label=p.replace("_", " ").title() + ":")
			ctrl = wx.TextCtrl(self.panel)
			self.puntuaciones_ctrls[p] = ctrl
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
		
		# Configurar eventos para cierre y teclado
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		
		# Inicializar la lista de amigos según el filtro ("Todos")
		self.reload_friends()
		if self.amigo_choice.GetCount() > 0:
			self.amigo_choice.SetSelection(0)
			self.on_select_amigo(None)
		
		# Guardar valores originales para detectar cambios
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
		"""Reordena la lista de amigos (de mayor a menor puntuación) y la filtra según el filtro seleccionado."""
		filtro = self.filtro_choice.GetStringSelection()  # "Todos", "Hombres", "Mujeres"
		all_friends = sorted(self.circulo.amigos, key=lambda a: sum(a.puntuaciones.values()), reverse=True)
		if filtro == "Todos":
			self.friends_sorted = all_friends
		elif filtro == "Hombres":
			self.friends_sorted = [a for a in all_friends if a.genero == "M"]
		else:  # "Mujeres"
			self.friends_sorted = [a for a in all_friends if a.genero == "F"]
		self.amigo_choice.Clear()
		self.amigo_choice.AppendItems([a.nombre for a in self.friends_sorted])
	
	def on_select_amigo(self, event):
		idx = self.amigo_choice.GetSelection()
		if idx == wx.NOT_FOUND:
			return
		amigo = self.friends_sorted[idx]
		self.nombre_ctrl.SetValue(amigo.nombre)
		# Seleccionar género según el dato del amigo
		if amigo.genero == "M":
			self.genero_choice.SetSelection(0)
		else:
			self.genero_choice.SetSelection(1)
		for key, ctrl in self.puntuaciones_ctrls.items():
			ctrl.SetValue(str(amigo.puntuaciones.get(key, 0)))
		# Actualizar el área de detalle usando un toString claro
		self.detail_text.SetLabel(self.formatear_detalle(amigo))
		# Guardar valores originales para detectar cambios
		self.original_nombre = amigo.nombre
		self.original_genero = amigo.genero
		self.original_puntuaciones = { key: str(amigo.puntuaciones.get(key, 0)) for key in self.lista_puntuaciones }
	
	def formatear_detalle(self, amigo):
		"""Devuelve un string formateado con información clara del amigo."""
		detalles = f"Nombre: {amigo.nombre}\n"
		detalles += f"Género: {'Hombre' if amigo.genero=='M' else 'Mujer'}\n"
		detalles += "Puntuaciones:\n"
		for key in self.lista_puntuaciones:
			detalles += f"  {key.replace('_',' ').title()}: {amigo.puntuaciones.get(key,0)}\n"
		detalles += f"Categoría: {amigo.categoria}"
		return detalles
	
	def has_unsaved_changes(self):
		if self.nombre_ctrl.GetValue().strip() != self.original_nombre:
			return True
		cur_gen = "M" if self.genero_choice.GetStringSelection() == "Hombre" else "F"
		if cur_gen != self.original_genero:
			return True
		for key, ctrl in self.puntuaciones_ctrls.items():
			if ctrl.GetValue().strip() != self.original_puntuaciones.get(key, ""):
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
			for key, ctrl in self.puntuaciones_ctrls.items():
				try:
					valor = int(ctrl.GetValue())
				except ValueError:
					raise ValueError(f"El valor de '{key.replace('_', ' ')}' debe ser un número entero.")
				nuevas_puntuaciones[key] = valor
			if not all(1 <= p <= 10 for p in nuevas_puntuaciones.values()):
				raise ValueError("Las puntuaciones deben estar entre 1 y 10.")
			amigo_actual = self.friends_sorted[idx]
			# Actualizar el objeto
			amigo_actual.editar_nombre(nuevo_nombre)
			amigo_actual.actualizar_puntuaciones(nuevas_puntuaciones)
			amigo_actual.editar_genero(nuevo_gen)
			self.circulo.guardar_amigos()
			detalle = "Amigo actualizado:\n" + self.formatear_detalle(amigo_actual)
			wx.MessageBox(detalle, "Información", wx.OK | wx.ICON_INFORMATION)
			# Recargar la lista y mantener la selección en el amigo actualizado
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
