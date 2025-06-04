import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_all_processos

class JanelaRelatorios:
    def __init__(self, root_toplevel):
        self.root = root_toplevel # 'root_toplevel' é a janela Toplevel passada
        self.root.title("Relatório de Processos") # Pode definir o título aqui também
        self.root.geometry("800x600") # E a geometria, se preferir

        # Frame principal para a lista de relatórios
        frame_principal_relatorio = ttk.LabelFrame(self.root, text="Detalhes dos Processos")
        frame_principal_relatorio.pack(padx=10, pady=10, fill="both", expand=True)

        # Definindo as colunas para o TreeView do relatório
        cols = ("id_processo", "numero_processo", "assunto", "data_criacao",
                "setor_responsavel", "status", "descricao_detalhada")
        self.tree_relatorio = ttk.Treeview(frame_principal_relatorio, columns=cols, show="headings")

        # Configurando os cabeçalhos e largura das colunas
        self.tree_relatorio.heading("id_processo", text="ID")
        self.tree_relatorio.column("id_processo", width=40, anchor="center", stretch=tk.NO)

        self.tree_relatorio.heading("numero_processo", text="Nº Processo")
        self.tree_relatorio.column("numero_processo", width=120, anchor="w")

        self.tree_relatorio.heading("assunto", text="Assunto")
        self.tree_relatorio.column("assunto", width=200, anchor="w")

        self.tree_relatorio.heading("data_criacao", text="Data Criação")
        self.tree_relatorio.column("data_criacao", width=100, anchor="center")

        self.tree_relatorio.heading("setor_responsavel", text="Setor")
        self.tree_relatorio.column("setor_responsavel", width=120, anchor="w")

        self.tree_relatorio.heading("status", text="Status")
        self.tree_relatorio.column("status", width=100, anchor="center")

        self.tree_relatorio.heading("descricao_detalhada", text="Descrição Detalhada")
        self.tree_relatorio.column("descricao_detalhada", width=250, anchor="w")

        # Adicionando Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_principal_relatorio, orient="vertical", command=self.tree_relatorio.yview)
        scrollbar_x = ttk.Scrollbar(frame_principal_relatorio, orient="horizontal", command=self.tree_relatorio.xview)
        self.tree_relatorio.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree_relatorio.pack(fill="both", expand=True)

        # Botão para fechar a janela de relatório
        btn_fechar = ttk.Button(self.root, text="Fechar Relatório", command=self.root.destroy)
        btn_fechar.pack(pady=10)

        # Carregar os dados no TreeView
        self.carregar_dados_no_relatorio()

    def carregar_dados_no_relatorio(self):
        """Busca todos os processos do banco e os exibe na TreeView do relatório."""
        for i in self.tree_relatorio.get_children():
            self.tree_relatorio.delete(i)

        try:
            processos = get_all_processos() # Certifique-se que esta função existe em database.py
            if processos:
                for proc in processos:
                    self.tree_relatorio.insert("", tk.END, values=proc)
            else:
                messagebox.showinfo("Relatório Vazio", "Não há processos cadastrados para exibir.", parent=self.root)
        except AttributeError: # Especificamente para o caso da função não existir no módulo database
            messagebox.showerror("Erro de Função BD",
                                 "A função 'get_all_processos_completos_db' não está definida em 'database.py'.",
                                 parent=self.root)
            print("ERRO: database.get_all_processos_completos_db() não foi encontrada.")
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados",
                                 f"Ocorreu um erro ao carregar os dados para o relatório: {e}",
                                 parent=self.root)
            print(f"Erro detalhado ao carregar relatório: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app_relatorios = JanelaRelatorios(root)
    app_relatorios.mainloop()