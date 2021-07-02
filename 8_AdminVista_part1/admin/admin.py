from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.lang import Builder

from sqlqueries import QueriesSQLite

Builder.load_file('admin/admin.kv')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    touch_deselect_last = BooleanProperty(True) 

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_codigo'].text = data['codigo']
		self.ids['_articulo'].text = data['nombre'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
		return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableProductoLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False

class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_nombre'].text = data['nombre'].title()
		self.ids['_username'].text = data['username']
		self.ids['_tipo'].text = str(data['tipo'])
		return super(SelectableUsuarioLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableUsuarioLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False

class AdminRV(RecycleView):
    def __init__(self, **kwargs):
        super(AdminRV, self).__init__(**kwargs)
        self.data=[]

    def agregar_datos(self,datos):
        for dato in datos:
            dato['seleccionado']=False
            self.data.append(dato)
        self.refresh_from_data()

    def dato_seleccionado(self):
        indice=-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice=i
                break
        return indice

class VistaProductos(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_productos, 1)

	def cargar_productos(self, *args):
		_productos=[]
		connection=QueriesSQLite.create_connection("pdvDB.sqlite")
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
		for producto in inventario_sql:
			_productos.append({'codigo': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]})
		self.ids.rv_productos.agregar_datos(_productos)


class VistaUsuarios(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_usuarios, 1)

	def cargar_usuarios(self, *args):
		_usuarios=[]
		connection=QueriesSQLite.create_connection("pdvDB.sqlite")
		usuarios_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
		for usuario in usuarios_sql:
			_usuarios.append({'nombre': usuario[1], 'username': usuario[0], 'password': usuario[2], 'tipo': usuario[3]})
		self.ids.rv_usuarios.agregar_datos(_usuarios)



class AdminWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.vista_actual='Productos'
		self.vista_manager=self.ids.vista_manager
		
		
	def cambiar_vista(self):
		if self.vista_actual=='Productos':
			self.vista_actual='Usuarios'
		else:
			self.vista_actual='Productos'
		self.vista_manager.current=self.vista_actual

	def signout(self):
		self.parent.parent.current='scrn_signin'

	def venta(self):
		self.parent.parent.current='scrn_ventas'


class AdminApp(App):
	def build(self):
		return AdminWindow()

if __name__=="__main__":
    AdminApp().run() 