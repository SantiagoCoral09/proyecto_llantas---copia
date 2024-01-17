import os
import sqlite3

def create_tables():
    # Obtener la ruta absoluta al directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta absoluta al archivo de la base de datos
    db_path = os.path.join(script_dir, 'proyectollantas.db')
    print("Esta es la ruta", script_dir)
    print("Esta es la ruta", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sentencias SQL para crear las tablas si no existen
    sentencias_sql = """
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            nom_usuario TEXT UNIQUE NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Productos (
            id INTEGER PRIMARY KEY,
            marca INTEGER NOT NULL,
            medida TEXT NOT NULL,
            costo REAL NOT NULL,
            descripcion TEXT NOT NULL,
            imagen TEXT NOT NULL,
            FOREIGN KEY (marca) REFERENCES Marca(id)
        );

        CREATE TABLE IF NOT EXISTS Productos_Carrito (
            id INTEGER PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_cantidad REAL NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES User(id),
            FOREIGN KEY (id_producto) REFERENCES Productos(id)
        );

        CREATE TABLE IF NOT EXISTS Compras (
            id INTEGER PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            precio REAL NOT NULL,
            celular TEXT NOT NULL,
            direccion TEXT NOT NULL,
            pago TeXT NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES User(id)
        );

        CREATE TABLE IF NOT EXISTS Productos_Compra (
            id INTEGER PRIMARY KEY,
            id_compra INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_cantidad REAL NOT NULL,
            FOREIGN KEY (id_compra) REFERENCES Compra(id),
            FOREIGN KEY (id_producto) REFERENCES Productos(id)
        );


        CREATE TABLE IF NOT EXISTS Marca (
            id INTEGER PRIMARY KEY,
            marca TEXT NOT NULL
        );

        INSERT INTO Productos(marca, medida, costo, descripcion, imagen) VALUES
            ('MICHELIN','205/55 R16', 530.000, 'Tecnologia llanta de alto desempeño, y con gran rendimiento en kilometraje.','catalogo3.PNG')
        ;
    """

    try:
        cursor.executescript(sentencias_sql)
        conn.commit()
        print('Se crearon las tablas...')
    except sqlite3.Error as e:
        print("Error al ejecutar las sentencias SQL:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    print("MAINNNNN")
    create_tables()
