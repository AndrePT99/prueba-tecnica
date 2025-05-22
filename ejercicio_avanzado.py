import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

def validar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def obtener_personajes():
    url = "https://rickandmortyapi.com/api/character"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        personajes = [char['name'] for char in data['results']]
        return personajes
    else:
        return []

def login():
    user = entry_usuario.get()
    pwd = entry_password.get()
    
    if validar_usuario(user, pwd):
        messagebox.showinfo("Login exitoso", f"Bienvenido, {user}")
        mostrar_personajes()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def mostrar_personajes():
    personajes = obtener_personajes()
    ventana_personajes = tk.Toplevel(root)
    ventana_personajes.title("Personajes Rick and Morty")
    
    label = tk.Label(ventana_personajes, text="Personajes:")
    label.pack()
    
    lista = tk.Listbox(ventana_personajes, width=50, height=15)
    lista.pack()
    
    for personaje in personajes:
        lista.insert(tk.END, personaje)

# ventana principal
root = tk.Tk()
root.title("Login")

# Etiqueta y campo usuario
tk.Label(root, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(root)
entry_usuario.pack(pady=5)

# Etiqueta y campo contraseña
tk.Label(root, text="Contraseña:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Botón login
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=20)

root.mainloop()
