# ui/estadisticas_dialog.py
import wx

class EstadisticasDialog(wx.Dialog):
    def __init__(self, parent, circulo, title="Estadísticas"):
        super(EstadisticasDialog, self).__init__(parent, title=title, size=(400, 500))
        self.circulo = circulo
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título
        title_txt = wx.StaticText(panel, label="Estadísticas del Círculo")
        font = title_txt.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font.SetPointSize(12)
        title_txt.SetFont(font)
        sizer.Add(title_txt, 0, wx.ALL | wx.CENTER, 10)

        # Calcular estadísticas
        total_amigos = len(self.circulo.amigos)
        hombres = sum(1 for a in self.circulo.amigos if a.genero == "M")
        mujeres = sum(1 for a in self.circulo.amigos if a.genero == "F")
        
        scores = [sum(a.puntuaciones.values()) for a in self.circulo.amigos]
        promedio = sum(scores) / total_amigos if total_amigos > 0 else 0
        
        categorias = {}
        for a in self.circulo.amigos:
            categorias[a.categoria] = categorias.get(a.categoria, 0) + 1

        # Mostrar datos
        stats_text = f"Total de Amigos: {total_amigos}\n"
        stats_text += f"Hombres: {hombres} ({hombres/total_amigos*100:.1f}%)\n" if total_amigos else "Hombres: 0\n"
        stats_text += f"Mujeres: {mujeres} ({mujeres/total_amigos*100:.1f}%)\n" if total_amigos else "Mujeres: 0\n"
        stats_text += f"Promedio de Puntuación: {promedio:.2f}\n\n"
        stats_text += "Distribución por Categoría:\n"
        for cat, count in categorias.items():
            stats_text += f"  - {cat}: {count}\n"

        text_ctrl = wx.TextCtrl(panel, value=stats_text, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # Botón Cerrar
        close_btn = wx.Button(panel, label="&Cerrar")
        close_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_OK))
        sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)
