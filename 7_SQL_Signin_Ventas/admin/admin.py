from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('admin/admin.kv')

class AdminWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(*kwargs)

	def ventas(self):
		self.parent.parent.current='scrn_ventas'

	def ventas(self):
		self.parent.parent.current='scrn_ventas'

class AdminApp(App):
	def build(self):
		return AdminWindow()

if __name__=="__main__":
	AdminApp().run()
