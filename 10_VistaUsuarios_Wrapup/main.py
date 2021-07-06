from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite
from signin.signin import SigninWindow
from admin.admin import AdminWindow
from ventas.ventas import VentasWindow

class MainWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(*kwargs)
		self.admin_widget=AdminWindow()
		self.ventas_widget=VentasWindow(self.admin_widget.actualizar_productos)
		self.signin_widget=SigninWindow(self.ventas_widget.poner_usuario)
		self.ids.scrn_signin.add_widget(self.signin_widget)
		self.ids.scrn_ventas.add_widget(self.ventas_widget)
		self.ids.scrn_admin.add_widget(self.admin_widget)

class MainApp(App):
	def build(self):
		return MainWindow()

if __name__=="__main__":
	MainApp().run()
