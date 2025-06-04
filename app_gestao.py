import tkinter as tk
from tkinter import ttk # Para widgets mais modernos como Treeview e Combobox
from tkinter import messagebox # Para caixas de diálogo de confirmação/erro

# Supondo que você tenha funções para interagir com o banco de dados em outro arquivo
# Exemplo: from database_manager import (
#    add_processo_db,
#    get_all_processos_db,
#    update_processo_db,
#    delete_processo_db,
#    create_processo_table # Certifique-se que a tabela é criada
# )

class JanelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Processos Administrativos")
        self.root.geometry("800x600") # Ajuste o tamanho conforme necessário

        # --- Frame de Entrada de Dados ---
        self.frame_entrada = ttk.LabelFrame(self.root, text="Detalhes do Processo")
        self.frame_entrada.pack(padx=10, pady=10, fill="x")

        # Labels e Entradas para os campos do processo
        # (id_processo será gerado pelo banco, numero_processo, assunto, data_criacao, setor_responsavel, status, descricao_detalhada)

        ttk.Label(self.frame_entrada, text="Nº Processo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_numero_processo = ttk.Entry(self.frame_entrada, width=40)
        self.entry_numero_processo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Assunto:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_assunto = ttk.Entry(self.frame_entrada, width=40)
        self.entry_assunto.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Data Criação (DD/MM/AAAA):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_data_criacao = ttk.Entry(self.frame_entrada, width=20)
        self.entry_data_criacao.grid(row=2, column=1, padx=5, pady=5, sticky="w") # Não esticar tanto

        ttk.Label(self.frame_entrada, text="Setor Responsável:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_setor_responsavel = ttk.Entry(self.frame_entrada, width=40)
        self.entry_setor_responsavel.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Status:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_status = ttk.Combobox(self.frame_entrada, values=["Aberto", "Em Andamento", "Pendente", "Concluído", "Arquivado"], width=37)
        self.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.combo_status.current(0) # Define um valor padrão

        ttk.Label(self.frame_entrada, text="Descrição Detalhada:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.text_descricao = tk.Text(self.frame_entrada, width=80, height=5)
        self.text_descricao.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Garantir que as colunas do frame de entrada se expandam adequadamente
        self.frame_entrada.columnconfigure(1, weight=1)
        self.frame_entrada.columnconfigure(3, weight=1)


        # --- Frame de Ações (Botões de Gerenciamento) ---
        self.frame_acoes = ttk.Frame(self.root)
        self.frame_acoes.pack(padx=10, pady=5, fill="x")

        self.btn_limpar_campos = ttk.Button(self.frame_acoes, text="Limpar Campos", command=self.limpar_campos_entrada)
        self.btn_limpar_campos.pack(side="left", padx=5)

        self.btn_cadastrar = ttk.Button(self.frame_acoes, text="Cadastrar Novo Processo", command=self.cadastrar_processo) # [cite: 5]
        self.btn_cadastrar.pack(side="left", padx=5)

        self.btn_salvar_edicao = ttk.Button(self.frame_acoes, text="Salvar Edição", command=self.salvar_edicao_processo, state="disabled") # [cite: 5]
        self.btn_salvar_edicao.pack(side="left", padx=5)

        self.btn_excluir = ttk.Button(self.frame_acoes, text="Excluir Processo", command=self.excluir_processo_selecionado, state="disabled") # [cite: 5]
        self.btn_excluir.pack(side="left", padx=5)

        # --- Frame da TreeView (Listagem de Processos) ---
        self.frame_lista = ttk.LabelFrame(self.root, text="Processos Cadastrados")
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        # Colunas da Treeview (o '#0' é uma coluna oculta para o ID, se você quiser)
        cols = ("id_processo", "numero_processo", "assunto", "data_criacao", "setor_responsavel", "status")
        self.tree_processos = ttk.Treeview(self.frame_lista, columns=cols, show="headings")

        # Definindo os cabeçalhos e largura das colunas
        self.tree_processos.heading("id_processo", text="ID")
        self.tree_processos.column("id_processo", width=50, anchor="center")
        self.tree_processos.heading("numero_processo", text="Nº Processo")
        self.tree_processos.column("numero_processo", width=100, anchor="center")
        self.tree_processos.heading("assunto", text="Assunto")
        self.tree_processos.column("assunto", width=200)
        self.tree_processos.heading("data_criacao", text="Data Criação")
        self.tree_processos.column("data_criacao", width=100, anchor="center")
        self.tree_processos.heading("setor_responsavel", text="Setor Responsável")
        self.tree_processos.column("setor_responsavel", width=150)
        self.tree_processos.heading("status", text="Status")
        self.tree_processos.column("status", width=100, anchor="center")

        # Adicionando Scrollbars à TreeView
        scrollbar_y = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree_processos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_lista, orient="horizontal", command=self.tree_processos.xview)
        self.tree_processos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree_processos.pack(fill="both", expand=True)

        # Evento para quando um item na TreeView é selecionado
        self.tree_processos.bind("<<TreeviewSelect>>", self.ao_selecionar_processo)

        # --- Botão para Relatórios ---
        self.frame_rodape = ttk.Frame(self.root)
        self.frame_rodape.pack(padx=10, pady=10, fill="x")

        self.btn_relatorios = ttk.Button(self.frame_rodape, text="Gerar Relatórios", command=self.abrir_janela_relatorios) # [cite: 4]
        self.btn_relatorios.pack(side="right", padx=5)

        # --- Carregar dados iniciais ---
        self.carregar_processos_na_treeview()

        # Variável para guardar o ID do item selecionado para edição/exclusão
        self.id_selecionado = None

    def limpar_campos_entrada(self):
        """Limpa todos os campos de entrada e a seleção da treeview."""
        self.entry_numero_processo.delete(0, tk.END)
        self.entry_assunto.delete(0, tk.END)
        self.entry_data_criacao.delete(0, tk.END)
        self.entry_setor_responsavel.delete(0, tk.END)
        self.combo_status.set('') # ou self.combo_status.current(0)
        self.text_descricao.delete("1.0", tk.END)
        self.entry_numero_processo.focus()

        if self.tree_processos.selection(): # Se houver algo selecionado
            self.tree_processos.selection_remove(self.tree_processos.selection()[0]) # Remove a seleção

        self.id_selecionado = None
        self.btn_salvar_edicao.config(state="disabled")
        self.btn_excluir.config(state="disabled")
        self.btn_cadastrar.config(state="normal")


    def carregar_processos_na_treeview(self):
        """Busca os processos no banco e os exibe na TreeView."""
        # Limpa a treeview antes de carregar novos dados
        for i in self.tree_processos.get_children():
            self.tree_processos.delete(i)

        # try:
        #     processos = get_all_processos_db() # Função do seu 'database_manager.py'
        #     for proc in processos:
        #         # A ordem aqui deve corresponder à ordem em 'cols' e como o DB retorna
        #         # Ex: (id, numero, assunto, data_criacao, setor, status, descricao - a descricao não vai pra treeview principal)
        #         self.tree_processos.insert("", tk.END, values=(proc[0], proc[1], proc[2], proc[3], proc[4], proc[5]))
        # except Exception as e:
        #     messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar os processos: {e}")
        print("Placeholder: Função carregar_processos_na_treeview")
        # Exemplo com dados fictícios:
        dados_ficticios = [
            (1, "PROC001", "Solicitação de Férias", "30/05/2025", "RH", "Aberto"),
            (2, "PROC002", "Reembolso de Despesas", "28/05/2025", "Financeiro", "Em Andamento"),
        ]
        for proc in dados_ficticios:
            self.tree_processos.insert("", tk.END, values=proc)


    def ao_selecionar_processo(self, event):
        """Chamado quando um processo é selecionado na TreeView."""
        selecionado = self.tree_processos.focus() # Pega o item focado/selecionado
        if not selecionado: # Se nada estiver selecionado (ex: após limpar seleção)
            self.limpar_campos_entrada() # Garante que os campos estejam limpos e botões no estado correto
            return

        valores = self.tree_processos.item(selecionado, "values")
        # A descrição detalhada não está na TreeView, precisaria buscá-la no banco se quisesse exibi-la
        # Por ora, vamos pegar apenas o que está visível

        self.limpar_campos_entrada() # Limpa antes de preencher

        self.id_selecionado = valores[0] # Guarda o ID do processo selecionado
        self.entry_numero_processo.insert(0, valores[1])
        self.entry_assunto.insert(0, valores[2])
        self.entry_data_criacao.insert(0, valores[3])
        self.entry_setor_responsavel.insert(0, valores[4])
        self.combo_status.set(valores[5])
        # self.text_descricao.insert("1.0", "Carregar descrição do banco de dados aqui se necessário")

        self.btn_salvar_edicao.config(state="normal")
        self.btn_excluir.config(state="normal")
        self.btn_cadastrar.config(state="disabled") # Desabilita cadastro ao selecionar um item

    def cadastrar_processo(self):
        """Coleta dados dos campos e chama a função de inserção no banco."""
        num_proc = self.entry_numero_processo.get()
        assunto = self.entry_assunto.get()
        data_criacao = self.entry_data_criacao.get()
        setor = self.entry_setor_responsavel.get()
        status = self.combo_status.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()

        if not all([num_proc, assunto, data_criacao, setor, status]):
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos obrigatórios.")
            return

        # try:
        #     add_processo_db(num_proc, assunto, data_criacao, setor, status, descricao) # Função do DB
        #     messagebox.showinfo("Sucesso", "Processo cadastrado com sucesso!")
        #     self.limpar_campos_entrada()
        #     self.carregar_processos_na_treeview()
        # except Exception as e: # Seria bom ter exceções mais específicas do DB
        #     messagebox.showerror("Erro no Cadastro", f"Não foi possível cadastrar o processo: {e}")
        print(f"Placeholder: Cadastrar Processo: {num_proc}, {assunto}, {data_criacao}, {setor}, {status}, {descricao}")
        messagebox.showinfo("Cadastro", "Placeholder: Processo seria cadastrado aqui.")
        self.limpar_campos_entrada()
        self.carregar_processos_na_treeview() # Atualiza a lista


    def salvar_edicao_processo(self):
        """Coleta dados dos campos e chama a função de atualização no banco."""
        if self.id_selecionado is None:
            messagebox.showwarning("Nenhum Processo", "Nenhum processo selecionado para editar.")
            return

        num_proc = self.entry_numero_processo.get()
        assunto = self.entry_assunto.get()
        data_criacao = self.entry_data_criacao.get()
        setor = self.entry_setor_responsavel.get()
        status = self.combo_status.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()

        if not all([num_proc, assunto, data_criacao, setor, status]):
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos obrigatórios.")
            return

        # try:
        #     update_processo_db(self.id_selecionado, num_proc, assunto, data_criacao, setor, status, descricao) # Função do DB
        #     messagebox.showinfo("Sucesso", "Processo atualizado com sucesso!")
        #     self.limpar_campos_entrada()
        #     self.carregar_processos_na_treeview()
        # except Exception as e:
        #     messagebox.showerror("Erro na Atualização", f"Não foi possível atualizar o processo: {e}")
        print(f"Placeholder: Salvar Edição do Processo ID {self.id_selecionado}: {num_proc}, {assunto}, {data_criacao}, {setor}, {status}, {descricao}")
        messagebox.showinfo("Edição", "Placeholder: Processo seria atualizado aqui.")
        self.limpar_campos_entrada()
        self.carregar_processos_na_treeview()


    def excluir_processo_selecionado(self):
        """Exclui o processo selecionado da TreeView e do banco."""
        if self.id_selecionado is None:
            messagebox.showwarning("Nenhum Processo", "Nenhum processo selecionado para excluir.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o processo ID {self.id_selecionado}?"):
            # try:
            #     delete_processo_db(self.id_selecionado) # Função do DB
            #     messagebox.showinfo("Sucesso", "Processo excluído com sucesso!")
            #     self.limpar_campos_entrada()
            #     self.carregar_processos_na_treeview()
            # except Exception as e:
            #     messagebox.showerror("Erro na Exclusão", f"Não foi possível excluir o processo: {e}")
            print(f"Placeholder: Excluir Processo ID {self.id_selecionado}")
            messagebox.showinfo("Exclusão", "Placeholder: Processo seria excluído aqui.")
            self.limpar_campos_entrada()
            self.carregar_processos_na_treeview()


    def abrir_janela_relatorios(self):
        # Aqui você chamaria a criação da sua janela de relatórios
        # Exemplo:
        # janela_relatorio_top_level = tk.Toplevel(self.root)
        # app_relatorio = JanelaRelatorios(janela_relatorio_top_level) # Supondo que você tenha uma classe JanelaRelatorios
        messagebox.showinfo("Relatórios", "Placeholder: A janela de relatórios seria aberta aqui.")
        print("Placeholder: Abrir Janela de Relatórios")


# Para testar esta janela isoladamente:
if __name__ == "__main__":
    # Idealmente, você chamaria sua função de criação da tabela aqui primeiro
    # Ex: create_processo_table()

    app_root = tk.Tk()
    main_app = JanelaPrincipal(app_root)
    app_root.mainloop()