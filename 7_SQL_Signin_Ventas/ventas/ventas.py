from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('ventas/ventas.kv')

from datetime import datetime, timedelta
from sqlqueries import QueriesSQLite

# inventario=[
# 	{'codigo': '111', 'nombre': 'leche 1L', 'precio': 20.0, 'cantidad': 20},
# 	{'codigo': '222', 'nombre': 'cereal 500g', 'precio': 50.5, 'cantidad': 15}, 
# 	{'codigo': '333', 'nombre': 'yogurt 1L', 'precio': 25.0, 'cantidad': 10},
# 	{'codigo': '444', 'nombre': 'helado 2L', 'precio': 80.0, 'cantidad': 20},
# 	{'codigo': '555', 'nombre': 'alimento para perro 20kg', 'precio': 750.0, 'cantidad': 5},
# 	{'codigo': '666', 'nombre': 'shampoo', 'precio': 100.0, 'cantidad': 25},
# 	{'codigo': '777', 'nombre': 'papel higiénico 4 rollos', 'precio': 35.5, 'cantidad': 30},
# 	{'codigo': '888', 'nombre': 'jabón para trastes', 'precio': 65.0, 'cantidad': 5},
# 	{'codigo': '999', 'nombre': 'refresco 600ml', 'precio': 15.0, 'cantidad': 10}
# ]

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
    	self.index = index
    	self.ids['_hashtag'].text = str(1+index)
    	self.ids['_articulo'].text = data['nombre'].capitalize()
    	self.ids['_cantidad'].text = str(data['cantidad_carrito'])
    	self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
    	self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
    	return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
        	rv.data[index]['seleccionado']=True
        else:
        	rv.data[index]['seleccionado']=False

class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
    	self.index = index
    	self.ids['_codigo'].text = data['codigo']
    	self.ids['_articulo'].text = data['nombre'].capitalize()
    	self.ids['_cantidad'].text = str(data['cantidad'])
    	self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
    	return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
        	rv.data[index]['seleccionado']=True
        else:
        	rv.data[index]['seleccionado']=False


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.modificar_producto=None

    def agregar_articulo(self, articulo):
    	articulo['seleccionado']=False
    	indice=-1
    	if self.data:
    		for i in range(len(self.data)):
    			if articulo['codigo']==self.data[i]['codigo']:
    				indice=i
    		if indice >=0:
    			self.data[indice]['cantidad_carrito']+=1
    			self.data[indice]['precio_total']=self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
    			self.refresh_from_data()
    		else:
	    		self.data.append(articulo)
    	else:
    		self.data.append(articulo)

    def eliminar_articulo(self):
    	indice=self.articulo_seleccionado()
    	precio=0
    	if indice>=0:
    		self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
    		precio=self.data[indice]['precio_total']
    		self.data.pop(indice)
    		self.refresh_from_data()
    	return precio

    def modificar_articulo(self):
    	indice=self.articulo_seleccionado()
    	if indice>=0:
    		popup=CambiarCantidadPopup(self.data[indice], self.actualizar_articulo)
    		popup.open()

    def actualizar_articulo(self, valor):
    	indice=self.articulo_seleccionado()
    	if indice>=0:
    		if valor==0:
    			self.data.pop(indice)
    			self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
    		else:
    			self.data[indice]['cantidad_carrito']=valor
    			self.data[indice]['precio_total']=self.data[indice]['precio']*valor
    		self.refresh_from_data()
    		nuevo_total=0
    		for data in self.data:
    			nuevo_total+=data['precio_total']
    		self.modificar_producto(False, nuevo_total)

    def articulo_seleccionado(self):
    	indice=-1
    	for i in range(len(self.data)):
    		if self.data[i]['seleccionado']:
    			indice=i
    			break
    	return indice


class ProductoPorNombrePopup(Popup):
	def __init__(self, input_nombre, agregar_producto_callback, **kwargs):
		super(ProductoPorNombrePopup, self).__init__(**kwargs)
		self.input_nombre=input_nombre
		self.agregar_producto=agregar_producto_callback

	def mostrar_articulos(self):
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
		self.open()
		for nombre in inventario_sql:
			if nombre[1].lower().find(self.input_nombre)>=0:
				producto={'codigo': nombre[0], 'nombre': nombre[1], 'precio': nombre[2], 'cantidad': nombre[3]}
				self.ids.rvs.agregar_articulo(producto)

	def seleccionar_articulo(self):
		indice=self.ids.rvs.articulo_seleccionado()
		if indice>=0:
			_articulo=self.ids.rvs.data[indice]
			articulo={}
			articulo['codigo']=_articulo['codigo']
			articulo['nombre']=_articulo['nombre']
			articulo['precio']=_articulo['precio']
			articulo['cantidad_carrito']=1
			articulo['cantidad_inventario']=_articulo['cantidad']
			articulo['precio_total']=_articulo['precio']
			if callable(self.agregar_producto):
				self.agregar_producto(articulo)
			self.dismiss()

class CambiarCantidadPopup(Popup):
	def __init__(self, data, actualizar_articulo_callback, **kwargs):
		super(CambiarCantidadPopup, self).__init__(**kwargs)
		self.data=data
		self.actualizar_articulo=actualizar_articulo_callback
		self.ids.info_nueva_cant_1.text = "Producto: " + self.data['nombre'].capitalize()
		self.ids.info_nueva_cant_2.text = "Cantidad: "+str(self.data['cantidad_carrito'])

	def validar_input(self, texto_input):
		try:
			nueva_cantidad=int(texto_input)
			self.ids.notificacion_no_valido.text=''
			self.actualizar_articulo(nueva_cantidad)
			self.dismiss()
		except:
			self.ids.notificacion_no_valido.text='Cantidad no valida'


class PagarPopup(Popup):
	def __init__(self, total, pagado_callback, **kwargs):
		super(PagarPopup, self).__init__(**kwargs)
		self.total=total
		self.pagado=pagado_callback
		self.ids.total.text= "{:.2f}".format(self.total)
		self.ids.boton_pagar.bind(on_release=self.dismiss)

	def mostrar_cambio(self):
		recibido= self.ids.recibido.text
		try:
			cambio=float(recibido)-float(self.total)
			if cambio>=0:
				self.ids.cambio.text="{:.2f}".format(cambio)
				self.ids.boton_pagar.disabled=False
			else:
				self.ids.cambio.text="Pago menor a cantidad a pagar"
		except:
			self.ids.cambio.text="Pago no valido"

class NuevaCompraPopup(Popup):
	def __init__(self, nueva_compra_callback, **kwargs):
		super(NuevaCompraPopup, self).__init__(**kwargs)
		self.nueva_compra=nueva_compra_callback
		self.ids.aceptar.bind(on_release=self.dismiss)


class VentasWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.total=0.0
		self.ids.rvs.modificar_producto=self.modificar_producto

		self.ahora=datetime.now()
		self.ids.fecha.text=self.ahora.strftime("%d/%m/%y")
		Clock.schedule_interval(self.actualizar_hora, 1)


	def agregar_producto_codigo(self, codigo):
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
		for producto in inventario_sql:
			if codigo==producto[0]:
				articulo={}
				articulo['codigo']=producto[0]
				articulo['nombre']=producto[1]
				articulo['precio']=producto[2]
				articulo['cantidad_carrito']=1
				articulo['cantidad_inventario']=producto[3]
				articulo['precio_total']=producto[2]
				self.agregar_producto(articulo)
				self.ids.buscar_codigo.text=''
				break

	def agregar_producto_nombre(self, nombre):
		self.ids.buscar_nombre.text=''
		popup=ProductoPorNombrePopup(nombre, self.agregar_producto)
		popup.mostrar_articulos()

	def agregar_producto(self, articulo):
		self.total+=articulo['precio']
		self.ids.sub_total.text= '$ '+"{:.2f}".format(self.total)
		self.ids.rvs.agregar_articulo(articulo)


	def eliminar_producto(self):
		menos_precio=self.ids.rvs.eliminar_articulo()
		self.total-=menos_precio
		self.ids.sub_total.text='$ '+"{:.2f}".format(self.total)

	def modificar_producto(self, cambio=True, nuevo_total=None):
		if cambio:	
			self.ids.rvs.modificar_articulo()
		else:
			self.total=nuevo_total
			self.ids.sub_total.text='$ '+"{:.2f}".format(self.total)

	def actualizar_hora(self, *args):
		self.ahora=self.ahora+timedelta(seconds=1)
		self.ids.hora.text=self.ahora.strftime("%H:%M:%S")		

	def pagar(self):
		if self.ids.rvs.data:
			popup=PagarPopup(self.total, self.pagado)
			popup.open()
		else:
			self.ids.notificacion_falla.text='No hay nada que pagar'

	def pagado(self):
		self.ids.notificacion_exito.text='Compra realizada con exito'
		self.ids.notificacion_falla.text=''
		self.ids.total.text="{:.2f}".format(self.total)
		self.ids.buscar_codigo.disabled=True
		self.ids.buscar_nombre.disabled=True
		self.ids.pagar.disabled=True
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		actualizar="""
		UPDATE
			productos
		SET
			cantidad=?
		WHERE
			codigo=?
		"""
		for producto in self.ids.rvs.data:
			nueva_cantidad=0
			if producto['cantidad_inventario']-producto['cantidad_carrito']>0:
				nueva_cantidad=producto['cantidad_inventario']-producto['cantidad_carrito']
			producto_tuple=(nueva_cantidad, producto['codigo'])
			QueriesSQLite.execute_query(connection, actualizar, producto_tuple)



	def nueva_compra(self, desde_popup=False):
		if desde_popup:
			self.ids.rvs.data=[]
			self.total=0.0
			self.ids.sub_total.text= '0.00'
			self.ids.total.text= '0.00'
			self.ids.notificacion_exito.text=''
			self.ids.notificacion_falla.text=''
			self.ids.buscar_codigo.disabled=False
			self.ids.buscar_nombre.disabled=False
			self.ids.pagar.disabled=False
			self.ids.rvs.refresh_from_data()
		elif len(self.ids.rvs.data):
			popup=NuevaCompraPopup(self.nueva_compra)
			popup.open()

	def admin(self):
		#self.parent.parent.current='scrn_admin'
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		select_products = "SELECT * from productos"
		productos = QueriesSQLite.execute_read_query(connection, select_products)
		for producto in productos:
			print(producto)


	def signout(self):
		if self.ids.rvs.data:
			self.ids.notificacion_falla.text='Compra abierta'
		else:
			self.parent.parent.current='scrn_singin'

	def poner_usuario(self, usuario):
		self.ids.bienvenido_label.text='Bienvenido '+usuario['nombre']

class VentasApp(App):
	def build(self):
		return VentasWindow()


if __name__=='__main__':
	VentasApp().run()
