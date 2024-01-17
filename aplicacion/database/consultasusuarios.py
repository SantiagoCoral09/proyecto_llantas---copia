# se define funciones para hacer consultas en la BD en la tabla proudctos
import sqlite3
from flask import current_app, session, request, flash, redirect, url_for

def consultar_usuario (username): # buscar si el user esta registrado en la base de datos.
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("SELECT * FROM User where nom_usuario = ?",(username,)) 
    usuarios=cursor.fetchone()#fetcholl 
    conexion.close()

    #retornar usuarios
    return usuarios



def registrar_usuario(nom_usuario, correo, contraseña):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    # Hash de la contraseña antes de almacenarla en la base de datos

    try:
        cursor.execute('INSERT INTO usuarios (nom_usuario, correo, contraseña) VALUES (?, ?, ?)',
                       (nom_usuario, correo, contraseña))
        conexion.commit()
        flash('¡Registro exitoso! Por favor, inicia sesión.')
    except sqlite3.IntegrityError:
        flash('El nombre de usuario o correo ya está en uso. Por favor, elige otros.')

    conexion.close()

def autenticar_usuario(nom_usuario, contraseña):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE nom_usuario = ?', (nom_usuario,))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario (usuario[3], contraseña):
        # Usuario autenticado correctamente
        session['usuario_id'] = usuario[0]
        flash('¡Inicio de sesión exitoso!')
        return True
    else:
        flash('Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.')
        return False




