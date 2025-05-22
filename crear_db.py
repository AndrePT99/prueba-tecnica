import sqlite3

def crear_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    
    # Crear tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)
    
    # Insertar usuarios de prueba (si no existen)
    usuarios_prueba = [
        ("andres", "1234"),
        ("maria", "abcd")
    ]
    
    for user, pwd in usuarios_prueba:
        cursor.execute("INSERT OR IGNORE INTO usuarios (username, password) VALUES (?, ?)", (user, pwd))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_db()
    print("Base de datos creada y usuarios insertados.")
