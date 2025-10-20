import sqlite3  # Usamos esta librería para trabajar con la base de datos

# Esta función crea la base de datos y las tablas si no existen
def init_database():
    conn = sqlite3.connect('database.db')  # Conectamos (o creamos) la base de datos
    c = conn.cursor()  # Preparamos para ejecutar comandos SQL
    
    # Creamos la tabla de inventario si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            proveedor TEXT NOT NULL,
            precio REAL NOT NULL,
            costo REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Creamos la tabla de ventas si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura INTEGER NOT NULL,
            nombre_articulo TEXT NOT NULL,
            valor_articulo REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL
        )
    ''')

    conn.commit()  # Guardamos los cambios
    conn.close()   # Cerramos la conexión con la base de datos

# Si ejecutamos este archivo directamente, inicializamos la base de datos
if __name__ == "__main__":
    init_database()
    print("Base de datos inicializada correctamente.")