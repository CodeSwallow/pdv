from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class VentasWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def agregar_producto_codigo(self, codigo):
		print("Se mando", codigo)

	def agregar_producto_nombre(self, nombre):
		print("Se mando", nombre)

	def eliminar_producto(self):
		print("eliminar_producto presionado")

	def modificar_producto(self):
		print("eliminar_producto presionado")

	def pagar(self):
		print("pagar")

	def nueva_compra(self):
		print("nueva_compra")

	def admin(self):
		print("Admin presionado")

	def signout(self):
		print("Signout presionado")

class VentasApp(App):
	def build(self):
		return VentasWindow()


if __name__=='__main__':
	VentasApp().run()