# eliminar_amigo_dialog.py

import wx

class EliminarAmigoDialog(wx.Dialog):
	def __init__(self, parent, circulo, title="Eliminar Amigo"):
		super(EliminarAmigoDialog, self).__init__(parent, title=title, size=(300, 200))
		
		self.circulo = circulo
		self.panel = wx.Panel(self)
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		wx.StaticText(self.panel, label="Seleccione un Amigo para eliminar:")
		self.amigo_choice = wx.Choice(self.panel, choices=[amigo.nombre for amigo in self.circulo.amigos])
		self.main_sizer.Add(self.amigo_choice, 0, wx.EXPAND | wx.ALL, 5)

		delete_button = wx.Button(self.panel, label="&Eliminar Amigo")
		delete_button.Bind(wx.EVT_BUTTON, self.on_confirm)
		self.main_sizer.Add(delete_button, 0, wx.EXPAND | wx.ALL, 5)
		
		self.panel.SetSizer(self.main_sizer)

		# Permitir cerrar el diálogo con Escape
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key)

	def on_key(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_CANCEL)
		else:
			event.Skip()

	def on_confirm(self, event):
		indice = self.amigo_choice.GetSelection()
		if indice == wx.NOT_FOUND:
			wx.MessageBox("No se ha seleccionado ningún amigo.", "Error", wx.OK | wx.ICON_ERROR)
			return
		amigo_nombre = self.circulo.amigos[indice].nombre
		mensaje = f"Está seguro de que desea eliminar a {amigo_nombre}?"
		if wx.MessageBox(mensaje, "Confirmar Eliminación", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
			self.resultado = indice
			self.EndModal(wx.ID_OK)
		else:
			wx.MessageBox("Operación cancelada.", "Información", wx.OK | wx.ICON_INFORMATION)

	def obtener_indice_seleccionado(self):
		return self.resultado
