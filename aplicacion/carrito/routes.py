from flask import current_app, render_template, session, redirect, url_for,request, flash
from aplicacion.carrito.forms import FormularioCompra

from aplicacion.database.consultasusuarios import consultar_usuario
from . import carrito
from aplicacion.database.consultasproductos import obtenerproductos,obtenerproducto
from aplicacion.carrito.carrito_compras import carrito_compras, Producto_Carrito, consultar_compra_id, registrar_compra, registrar_producto_compra
from flask_paginate import Pagination, get_page_args
from flask_babel import _
from flask_mail import Mail, Message
from aplicacion.config.email import mail


@carrito.route('/productos')
def productos():
   if "username" not in session:
      return redirect(url_for("cuenta.login"))
   
   productos=obtenerproductos()
   # Configurar la paginación
   page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
   
   # Establecer la cantidad de productos por página (ajusta según tus necesidades)
   per_page = 3
   total = len(productos)
   pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

   # Calcular el índice de inicio y final para los productos en la página actual
   start = (page - 1) * per_page
   end = start + per_page

   # Obtén los productos para la página actual
   productos_paginados = productos[start:end]

   # print(productos)
   usuario=consultar_usuario(username=session["username"])
   # carrito_compras.id_usuario=usuario[0]
   carrito_compras.cargar_carrito()
   # print(f"Carrito actual: {carrito_compras.productos}")
   return render_template('carrito.html', productos=productos_paginados,pagination=pagination,carrito_compras=carrito_compras)

@carrito.route('/agregar_producto/<id_producto>', methods=["GET", "POST"])
def agregar_producto(id_producto):
   if "username" not in session:
      return redirect(url_for("cuenta.login"))
   if request.method=="POST":      
      usuario=consultar_usuario(session["username"])

      carrito_compras.id_usuario=usuario[0]
      producto=obtenerproducto(id_producto)
      print(f"Producto id: {producto[0]}")
      precio_producto=producto[3]

      try:
         cantidad = int(request.form.get(f'cantidad_{id_producto}'))
         print(f"cantidad: {cantidad}")
         if cantidad>0:
            
            precio_x_cantidad=cantidad*precio_producto

            producto_carrito=Producto_Carrito(usuario[0],id_producto, cantidad,precio_x_cantidad)
            carrito_compras.agregar_producto(producto_carrito)
            print(carrito_compras)
            # flash("Producto Agregado","success")
            return redirect(url_for("carrito.productos"))
         else:
            flash(_("Error la cantidad no puede ser menor o igual a 0"), "danger")
            return redirect(url_for("carrito.productos"))
      except Exception as e:
         flash(f"Error de cantidad: Debe ser un número mayor a cero {e}","danger")
   return redirect(url_for("carrito.productos"))

@carrito.route("/modificar_producto/<id_producto_carrito>",methods=["GET","POST"])
def modificar_producto(id_producto_carrito):
   # Se recibe el id del producto de la tabla productos_carrito
   if "username" not in session:
      return redirect(url_for("cuenta.login"))
   if request.method=="POST":
      usuario=consultar_usuario(session["username"])
      id_usuario=usuario[0]
      carrito_compras.id_usuario=usuario[0]

      print(f"ProductoCarrito id: {id_producto_carrito}")


      try:
         cantidad = int(request.form.get(f'cantidad_{id_producto_carrito}'))
         print(f"cantidad nueva: {cantidad}")
         if cantidad>0:
            

            carrito_compras.modificar_producto(id_producto_carrito, id_usuario, cantidad)
            # print(carrito_compras)
            # flash("Producto Agregado","success")
            return redirect(url_for("carrito.productos"))
         else:
            flash(_("Error la cantidad no puede ser menor o igual a 0"), "danger")
            return redirect(url_for("carrito.productos"))
      except Exception as e:
         flash(f"Error de cantidad: Debe ser un número mayor a cero {e}","danger")

   return redirect(url_for("carrito.productos"))

@carrito.route("/eliminar_producto/<id_producto_carrito>",methods=["GET","POST"])
def eliminar_producto(id_producto_carrito):
   if "username" not in session:
      return redirect(url_for("cuenta.login"))

   usuario=consultar_usuario(session["username"])
   carrito_compras.id_usuario=usuario[0]   
   carrito_compras.eliminar_producto(id_producto_carrito)
   flash(_("Se eliminó el producto del carrito"),"success")
   return redirect(url_for("carrito.productos"))

@carrito.route("/comprar",methods=["GET","POST"])
def comprar():
   if "username" not in session:
      return redirect(url_for("cuenta.login"))
   
   form = FormularioCompra(request.form)
   usuario=consultar_usuario(session["username"])
   carrito_compras.id_usuario=usuario[0]   
   carrito_compras.cargar_carrito()
   id_usuario=usuario[0]   
   email=usuario[2]
   # print(carrito_compras)

   if form.validate_on_submit():
      celular = form.celular.data
      direccion = form.direccion.data
      pago = form.pago.data
      print(celular,direccion,pago)

      # Primero registramos la compra en general
      id_compra=registrar_compra(id_usuario,carrito_compras.valor_total,celular,direccion,pago)
      if id_compra:
         compra=consultar_compra_id(id_compra)
         copia_carrito_compras=carrito_compras
          # Para enviar un corrreo de registro exitoso
         msg = Message(_('Gracias por comprar en Llantas Express!!'),
                     sender=current_app.config['MAIL_USERNAME'],
                     recipients=[email])
         # print(f"Mensaje... {msg}")
         msg.html = render_template('email_compra.html', username=email,carrito_compras=copia_carrito_compras,compra=compra)
         mail.send(msg)
         # Se logró registrar la compra, debemos registrar cada producto del carrito a la comparra
         for producto in carrito_compras.productos:
            if registrar_producto_compra(id_compra,producto[1],producto[7],producto[8]):
               # Se logró registarr el producto del carrito rn la compra, entonces se lo saca del carrito

               carrito_compras.eliminar_producto(producto[0])
         carrito_compras.cargar_carrito()
         if carrito_compras.cantidad_productos==0:
            # Ya se registró exitosamente toda la compra
            flash(_("Se ha registrado su compra exitosamente"),"success")

            return redirect(url_for("carrito.productos"))
      else:
         # Ha ocurrido un error en registrar la compra en general   #
         flash(_("Ha ocurrido un error"),"warning") 
   return render_template('comprar.html', carrito_compras=carrito_compras, form=form)
