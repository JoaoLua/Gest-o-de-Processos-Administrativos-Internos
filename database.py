import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

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



#Operações login e cadastro
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

# processos crud

def add_processo(numero_processo, assunto, data_criacao, setor_responsavel, status, descricao_detalhada):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO processos (
                numero_processo, 
                assunto, 
                data_criacao, 
                setor_responsavel,      
                status, 
                descricao_detalhada
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (numero_processo, assunto, data_criacao, setor_responsavel, status, descricao_detalhada))
        conn.commit()
        conn.close()
        return True  # Agora a interface saberá que deu certo!
    except Exception as e:
        print(f"Erro ao inserir processo: {e}")
        return False

def get_all_processos():
    """Busca todos os processos do banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Seleciona apenas os campos que podem ser úteis para uma listagem inicial/TreeView
        cursor.execute("SELECT id_processo, numero_processo, assunto, data_criacao, setor_responsavel, status FROM processos ORDER BY id_processo DESC")
        processos = cursor.fetchall()
        return processos
    except sqlite3.Error as e:
        print(f"Erro ao buscar processos: {e}")
        return [] # Retorna lista vazia em caso de erro
    finally:
        conn.close()

def get_processo_by_id(id_processo):
    """Busca um processo específico pelo seu ID, incluindo todos os campos."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM processos WHERE id_processo = ?", (id_processo,))
        processo = cursor.fetchone() # Retorna uma tupla ou None
        return processo
    except sqlite3.Error as e:
        print(f"Erro ao buscar processo por ID ({id_processo}): {e}")
        return None
    finally:
        conn.close()

def update_processo(id_processo, numero_processo, assunto, data_criacao, setor_responsavel, status, descricao_detalhada):
    """Atualiza um processo existente no banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE processos
            SET numero_processo = ?,
                assunto = ?,
                data_criacao = ?,
                setor_responsavel = ?,
                status = ?,
                descricao_detalhada = ?
            WHERE id_processo = ?
        """, (numero_processo, assunto, data_criacao, setor_responsavel, status, descricao_detalhada, id_processo))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Nenhum processo encontrado com ID {id_processo} para atualizar.")
            return False # Nenhum registro foi atualizado (ID pode não existir)
        print(f"Processo ID {id_processo} atualizado com sucesso.")
        return True
    except sqlite3.IntegrityError:
        print(f"Erro: Número de processo '{numero_processo}' já existe para outro registro.")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao atualizar processo ID {id_processo}: {e}")
        return False
    finally:
        conn.close()

def delete_processo(id_processo):
    """Deleta um processo do banco de dados pelo seu ID."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM processos WHERE id_processo = ?", (id_processo,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Nenhum processo encontrado com ID {id_processo} para deletar.")
            return False # Nenhum registro foi deletado
        print(f"Processo ID {id_processo} deletado com sucesso.")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao deletar processo ID {id_processo}: {e}")
        return False
    finally:
        conn.close()

def inicializar_banco():
    criar_tabela_usuarios()
    criar_tabela_processos()