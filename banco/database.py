import sqlite3
import os 

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), 'banco.db')
def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def criar_tabela_usuarios(): #regitro tabela usuarios
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def criar_tabela_processos():  # registro tabela processos
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processos (
                id_processo INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_processo TEXT UNIQUE NOT NULL,
                assunto TEXT NOT NULL,
                data_criacao TEXT,
                setor_responsavel TEXT,
                status TEXT,
                descricao_detalhada TEXT
            )
        """)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
 
def inicializar_banco():
    criar_tabela_usuarios()
    criar_tabela_processos()