from tkinter import ttk
from tkinter import *

import sqlite3 as sq

class Product:

    dbNombre = 'database.db'

    def __init__(self):

        # Ventana

        self.ventana = Tk()
        self.ventana.title('Lista de Productos')

        # Frame Contenedor

        frame =LabelFrame(self.ventana, text='Registra Un Nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Entrada Nombre

        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column = 1)

        # Entrada Precio

        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Boton agregar producto

        ttk.Button(frame, text='Guardar Producto', command=self.agregarProducto).grid(row=3, columnspan=2, sticky= W + E)

        # Mensaje Salida

        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky= W + E)

        # Tabla

        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        # Botones

        ttk.Button(text='BORRAR', command=self.eliminarProducto).grid(row=5, column=0, sticky= W + E)
        ttk.Button(text='EDITAR', command=self.editarProducto).grid(row=5, column=1, sticky= W + E)

        # Llenando las filas
        
        self.getProductos()

        ####

        self.ventana.mainloop()

    def ejecutarConsulta(self, consulta, parametros = ()):

        with sq.connect(self.dbNombre) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(consulta, parametros)
            conn.commit()
            return resultado

    def getProductos(self):

        # Limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Consulta de datos
        query = 'SELECT * FROM Producto ORDER BY nombre ASC'
        dbFilas = self.ejecutarConsulta(query)
        
        # Completando datos
        for fila in dbFilas:
            self.tree.insert('', 0, text = fila[1], values = fila[2])

    def validarEntrada(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0
    
    def agregarProducto(self):
        
        if self.validarEntrada():
            query = 'INSERT INTO Producto VALUES(NULL, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get())
            self.ejecutarConsulta(query, parametros)
            self.mensaje['text'] = 'El producto {} ha sido agregado'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje['text'] = 'El nombre y el precio son requeridos'
        self.getProductos()

    def eliminarProducto(self):
        
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un registro'
            return
        self.mensaje['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Producto WHERE nombre = ?'
        self.ejecutarConsulta(query, (name, ))
        self.mensaje['text'] = 'El registro {} ha sido eliminado'.format(name)
        self.getProductos()

    def editarProducto(self):
        
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un registro'
            return
        
        nombreActual = self.tree.item(self.tree.selection())['text']
        precioViejo = self.tree.item(self.tree.selection())['values'][0]

        self.ventanaEdicion = Toplevel()
        self.ventanaEdicion.title('Editar Producto')

        # Nombre viejo
        Label(self.ventanaEdicion, text="Nombre anterior").grid(row=0, column=1)
        Entry(self.ventanaEdicion, textvariable=StringVar(self.ventanaEdicion, value=nombreActual), state='readonly').grid(row=0, column=2)

        # Nombre nuevo
        Label(self.ventanaEdicion, text='Nombre nuevo').grid(row=1, column=1)
        nuevoNombre = Entry(self.ventanaEdicion)
        nuevoNombre.grid(row=1, column=2)

        # Precio viejo
        Label(self.ventanaEdicion, text='Precio anterior').grid(row=2, column=1)
        Entry(self.ventanaEdicion, textvariable=StringVar(self.ventanaEdicion, value=precioViejo), state='readonly').grid(row=2, column=2)

        # Precio nuevo
        Label(self.ventanaEdicion, text='Precio nuevo').grid(row=3, column=1)
        nuevoPrecio = Entry(self.ventanaEdicion)
        nuevoPrecio.grid(row=3, column=2)

        # Boton Actualizar
        Button(self.ventanaEdicion, text='Actualizar', command=lambda:self.editarRegistro(nombreActual, nuevoNombre.get(), nuevoPrecio.get(), precioViejo)).grid(row=4, column=2, sticky= W)

    def editarRegistro(self, nombre, nuevoNombre, nuevoPrecio, precioViejo):
        query = 'UPDATE Producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parametros = (nuevoNombre, nuevoPrecio, nombre, precioViejo)
        self.ejecutarConsulta(query, parametros)
        self.ventanaEdicion.destroy()
        self.mensaje['text'] = 'Registro actualizado'.format(nombre)
        self.getProductos()

########################################################################################

app = Product()
