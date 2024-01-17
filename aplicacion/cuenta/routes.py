import os
from flask import current_app, render_template, request, url_for, redirect, flash, session
import sqlite3
from . import cuenta
from aplicacion.cuenta.forms import Formulariologin, Formularioregistro
from aplicacion.database.consultasusuarios import consultar_usuario
from flask_babel import _
from flask_mail import Mail,Message
from aplicacion.config.email import mail


@cuenta.route('/login', methods=["GET", "POST"])
def login():
    if "username" in session:
        return  redirect(url_for("inicio.inicio"))
    
    form = Formulariologin(request.form)

    if form.validate_on_submit():
        username = form.usuariologin.data
        password = form.contraseñalogin.data

        usuario_existe=consultar_usuario(username)
        print(f"Intentando acceder a la base de datos  con usuario: {usuario_existe} ")

        if usuario_existe:
            print("Usuario existe")
            if usuario_existe[3] == password:
                flash(_('Inicio de sesión exitoso'), 'success')
                session["username"]=username
                return redirect(url_for("carrito.productos"))
            else:
                #contraseña incorrecta 
                flash(_("La contraseña no es correcta"), "danger")
        else:
            flash(_('Usuario no esta registrado'), 'danger')

    return render_template('cuentalog.html', form=form)

@cuenta.route('/registro', methods=["GET", "POST"])
def registro():
    form = Formularioregistro(request.form)

    if form.validate_on_submit():
        usuarioreg = form.usuarioreg.data
        email = form.correoreg.data
        password = form.contraseñareg.data

        conn = sqlite3.connect('aplicacion/database/proyectollantas.db')
        cursor = conn.cursor()

        # Verificar si el usuario ya existe
        cursor.execute('SELECT * FROM User WHERE nom_usuario = ? OR correo = ?', (usuarioreg, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash(_('Usuario o correo electrónico ya registrados'), 'danger')
        else:
            # Insertar la contraseña en texto plano en la base de datos
            cursor.execute('INSERT INTO User (nom_usuario, correo, contraseña) VALUES (?, ?, ?)', (usuarioreg, email, password))
            conn.commit()
            flash(_('Registro exitoso. ¡Ahora puedes iniciar sesión!'), 'success')

            # Para enviar un corrreo de registro exitoso
            msg = Message(_('Te has registrado en nuestra plataforma de Llantas Express!'),
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[email])
            # print(f"Mensaje... {msg}")
            msg.html = render_template('email.html', username=usuarioreg)
            mail.send(msg)

            return redirect(url_for("cuenta.login"))

    return render_template('registro.html', form=form)

@cuenta.route('/cerrar_sesion')
def cerrar_sesion():
    if "username" in session:
        session.pop("username",None)
    return redirect(url_for("cuenta.login"))   

