from banco.database import conectar
import sqlite3

def cadastrar_usuario(nome, email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Email já cadastrado

def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario