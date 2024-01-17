import json
import sqlite3
from flask import current_app, flash, session
from aplicacion.database.consultasproductos import obtenerproducto
from aplicacion.database.consultasusuarios import consultar_usuario
from datetime import datetime
from flask_babel import _


class Producto_Carrito:
    def __init__(self,id_usuario,id_producto,cantidad,precio_cantidad):
        self.id_usuario=id_usuario
        self.id_producto=id_producto
        self.cantidad=cantidad
        self.precio_cantidad=precio_cantidad
        self.marca=obtenerproducto(id_producto)[1]
        self.medida=obtenerproducto(id_producto)[2]
        self.precio=obtenerproducto(id_producto)[3]
        self.descripcion=obtenerproducto(id_producto)[4]
        self.imagen=obtenerproducto(id_producto)[5]
    
    def __str__(self) -> str:
        return f"{self.id_producto}: {(self.marca).upper()} {self.medida}, {self.cantidad} und (${self.precio_cantidad})"

class Carrito:
    def __init__(self):
        self.id_usuario=0
        self.cantidad_productos=0
        self.valor_total=0
        self.productos=None

    def agregar_producto (self,producto: Producto_Carrito):
        producto_existe=obtener_producto_carrito(producto.id_producto,producto.id_usuario)
        print(f"Pproducto: {producto_existe}")
        if producto_existe:
            id_producto_carrito=producto_existe[0]
            cantidad_antes=producto_existe[7]
            precio_cantidad_antes=producto_existe[8]
            nueva_cantidad=cantidad_antes+producto.cantidad
            nueva_precio_cantidad=precio_cantidad_antes+producto.precio_cantidad
            actualizar_producto_carrito(nueva_cantidad,nueva_precio_cantidad,id_producto_carrito)
            flash(_("Se actualizó la cantidad del producto"),"success")
            
        else:
            agregar_producto_carrito(producto)
            flash(_("Se agregó el producto al carrito"),"success")

    def modificar_producto(self,id_producto_carrito,id_usuario,cantidad):
        producto_existe=obtener_producto_carrito_por_id(id_producto_carrito)
        if producto_existe:
            precio_unidad=producto_existe[4]
            precio_cantidad=precio_unidad*cantidad
            actualizar_producto_carrito(cantidad,precio_cantidad,id_producto_carrito)
            flash(_("Se modificó el producto del carrito"),"success")
        else:
            print("No existe el producto")

    def eliminar_producto(self,id_producto_carrito):
        producto_existe=obtener_producto_carrito_por_id(id_producto_carrito)
        if producto_existe:
            eliminar_producto_carrito(id_producto_carrito)
            
        else:
            print("No existe el producto")

    


    def __str__(self) -> str:
        # self.cargar_carrito()
        cadena="Carrito:"
        if self.productos:
            for item in self.productos:
                cadena+=f"\n- {item}"
        return cadena
    
    def cargar_carrito(self):
        if "username" in session:
            usuario=consultar_usuario(session["username"])
            self.id_usuario=usuario[0]
            self.productos=None
            self.cantidad_productos=0
            self.valor_total=0
            self.productos=obtener_productos_carrito(self.id_usuario)
            # print(f"Cargar carrito {self.productos}")

            for producto in self.productos:
                self.cantidad_productos+=int(producto[7])
                self.valor_total+=producto[8]




# ******FUNCIONES PARA MANEJAR LA BASE DE DATOS************
def obtener_productos_carrito(id_usuario):
    # Obtener todos los productos del carrito que pertenecen a un usuario
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("""
    SELECT
        PC.id AS producto_carrito_id,
        P.id AS producto_id,
        M.marca AS nombre_marca,
        P.medida,
        P.costo,
        P.descripcion,
        P.imagen,
        PC.cantidad,
        PC.precio_cantidad
    FROM Productos_Carrito PC
    JOIN Productos P ON PC.id_producto = P.id
    JOIN Marca M ON P.marca = M.id
    WHERE PC.id_usuario = ?
    """,(id_usuario,)) 
    productos=cursor.fetchall()#fetcholl varios productos-guardar productos de la consulta
    conexion.close()

    #retornar productos
    return productos

def obtener_producto_carrito(id_producto,id_usuario):
    # Verificar si un usuario agregó un producto a su carrito
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("""
    SELECT
        PC.id AS producto_carrito_id,
        P.id AS producto_id,
        M.marca AS nombre_marca,
        P.medida,
        P.costo,
        P.descripcion,
        P.imagen,
        PC.cantidad,
        PC.precio_cantidad
    FROM Productos_Carrito PC
    JOIN Productos P ON PC.id_producto = P.id
    JOIN Marca M ON P.marca = M.id
    WHERE PC.id_producto = ? AND PC.id_usuario=?
    """,(id_producto,id_usuario,)) 
    productos=cursor.fetchone()#fetcholl varios productos-guardar productos de la consulta
    conexion.close()

    #retornar productos
    return productos

def obtener_producto_carrito_por_id(id_producto_carrito):
    # Verificar si un usuario agregó un producto a su carrito
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("""
    SELECT
        PC.id AS producto_carrito_id,
        P.id AS producto_id,
        M.marca AS nombre_marca,
        P.medida,
        P.costo,
        P.descripcion,
        P.imagen,
        PC.cantidad,
        PC.precio_cantidad
    FROM Productos_Carrito PC
    JOIN Productos P ON PC.id_producto = P.id
    JOIN Marca M ON P.marca = M.id
    WHERE PC.id = ?    """,(id_producto_carrito,)) 
    productos=cursor.fetchone()#fetcholl varios productos-guardar productos de la consulta
    conexion.close()

    #retornar productos
    return productos

def agregar_producto_carrito(producto_carrito):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        cursor.execute("INSERT INTO Productos_Carrito (id_usuario,id_producto, cantidad, precio_cantidad) VALUES (?,?,?,?)",(producto_carrito.id_usuario,producto_carrito.id_producto,producto_carrito.cantidad,producto_carrito.precio_cantidad,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return False
    
def actualizar_producto_carrito(cantidad,precio_cantidad,id_producto_carrito):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        cursor.execute("UPDATE Productos_Carrito SET cantidad=?, precio_cantidad=? WHERE id=?",(cantidad,precio_cantidad,id_producto_carrito))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return False

def eliminar_producto_carrito(id_producto_carrito):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        cursor.execute("DELETE FROM Productos_Carrito WHERE id=?",(id_producto_carrito,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return False

def vaciar_carrito(id_usuario):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        cursor.execute("DELETE * FROM Productos_Carrito WHERE id_usuario=?",(id_usuario,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return False

def registrar_compra(id_usuario,precio,celular,direccion,pago):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        fecha=datetime.now()
        cursor.execute("INSERT INTO Compras (id_usuario,fecha,precio,celular,direccion,pago) VALUES (?,?,?,?,?,?)",(id_usuario,fecha,precio,celular,direccion,pago,))
        conexion.commit()
        id_compra = cursor.lastrowid

        conexion.close()
        return id_compra
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return None
    
def consultar_compra_id(id_compra):
    ruta=current_app.config["DATABASE_URI"].replace('sqlite:///','')
    conexion=sqlite3.connect(ruta)
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM Compras WHERE id=?",(id_compra,))
    compra=cursor.fetchone()
    conexion.close()
    return compra

def registrar_producto_compra(id_compra,id_producto,cantidad,precio_cantidad):
    try:
        ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
        conexion=sqlite3.connect(ruta)

        cursor=conexion.cursor()#para relizar consultas mediante un cursor
        cursor.execute("INSERT INTO Productos_Compra (id_compra,id_producto,cantidad,precio_cantidad) VALUES (?,?,?,?)",(id_compra,id_producto,cantidad,precio_cantidad,))
        conexion.commit()

        conexion.close()
        return True
    except Exception as e:
        flash(f"Error al insertar el producto en el carrito {e}")
        return False

carrito_compras=Carrito()
