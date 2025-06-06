from banco.database import conectar
import sqlite3

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
