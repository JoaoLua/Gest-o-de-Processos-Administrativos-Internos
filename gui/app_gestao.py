import tkinter as tk
from tkinter import ttk, messagebox
from banco.database import inicializar_banco
from verificacoes.gestao import add_processo, get_all_processos, get_processo_by_id, update_processo, delete_processo
from gui.app_relatorios import JanelaRelatorios

class JanelaGestao:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Processos Administrativos")
        self.root.geometry("800x600")

        self.id_selecionado = None

        self.criar_interface()
        self.carregar_processos_na_treeview()

    def criar_interface(self):
        # Frame de Entrada
        self.frame_entrada = ttk.LabelFrame(self.root, text="Detalhes do Processo")
        self.frame_entrada.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.frame_entrada, text="Nº Processo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_numero_processo = ttk.Entry(self.frame_entrada, width=40)
        self.entry_numero_processo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Assunto:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_assunto = ttk.Entry(self.frame_entrada, width=40)
        self.entry_assunto.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Data Criação (DD/MM/AAAA):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_data_criacao = ttk.Entry(self.frame_entrada, width=20)
        self.entry_data_criacao.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.frame_entrada, text="Setor Responsável:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_setor_responsavel = ttk.Entry(self.frame_entrada, width=40)
        self.entry_setor_responsavel.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_entrada, text="Status:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_status = ttk.Combobox(self.frame_entrada, values=["Aberto", "Em Andamento", "Pendente", "Concluído", "Arquivado"], width=37, state="readonly")
        self.combo_status.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.combo_status.current(0)

        ttk.Label(self.frame_entrada, text="Descrição Detalhada:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.text_descricao = tk.Text(self.frame_entrada, width=80, height=5, wrap=tk.WORD)
        self.text_descricao.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        desc_scrollbar = ttk.Scrollbar(self.frame_entrada, orient="vertical", command=self.text_descricao.yview)
        desc_scrollbar.grid(row=3, column=4, sticky="ns", pady=5)
        self.text_descricao.configure(yscrollcommand=desc_scrollbar.set)

        self.frame_entrada.columnconfigure(1, weight=1)
        self.frame_entrada.columnconfigure(3, weight=1)

        # Frame Ações
        self.frame_acoes = ttk.Frame(self.root)
        self.frame_acoes.pack(padx=10, pady=5, fill="x")

        self.btn_limpar_campos = ttk.Button(self.frame_acoes, text="Limpar Campos", command=self.limpar_campos_entrada)
        self.btn_limpar_campos.pack(side="left", padx=5)

        self.btn_cadastrar = ttk.Button(self.frame_acoes, text="Cadastrar Novo Processo", command=self.cadastrar_processo)
        self.btn_cadastrar.pack(side="left", padx=5)

        self.btn_salvar_edicao = ttk.Button(self.frame_acoes, text="Salvar Edição", command=self.salvar_edicao_processo, state="disabled")
        self.btn_salvar_edicao.pack(side="left", padx=5)

        self.btn_excluir = ttk.Button(self.frame_acoes, text="Excluir Processo", command=self.excluir_processo_selecionado, state="disabled")
        self.btn_excluir.pack(side="left", padx=5)

        # Frame Lista
        self.frame_lista = ttk.LabelFrame(self.root, text="Processos Cadastrados")
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        cols = ("id_processo", "numero_processo", "assunto", "data_criacao", "setor_responsavel", "status")
        self.tree_processos = ttk.Treeview(self.frame_lista, columns=cols, show="headings")

        for col in cols:
            self.tree_processos.heading(col, text=col.replace("_", " ").title())

        self.tree_processos.column("id_processo", width=50, anchor="center", stretch=tk.NO)
        self.tree_processos.column("numero_processo", width=120)
        self.tree_processos.column("assunto", width=250)
        self.tree_processos.column("data_criacao", width=100, anchor="center")
        self.tree_processos.column("setor_responsavel", width=120)
        self.tree_processos.column("status", width=100, anchor="center")

        scrollbar_y = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree_processos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_lista, orient="horizontal", command=self.tree_processos.xview)
        self.tree_processos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree_processos.pack(fill="both", expand=True)

        self.tree_processos.bind("<<TreeviewSelect>>", self.ao_selecionar_processo)

        # Frame Rodapé
        self.frame_rodape = ttk.Frame(self.root)
        self.frame_rodape.pack(padx=10, pady=10, fill="x")

        self.btn_relatorios = ttk.Button(self.frame_rodape, text="Gerar Relatórios", command=self.open_relatorios)
        self.btn_relatorios.pack(side="right", padx=5)

    def open_relatorios(self):
        self.root.destroy()
        relatorios_root = tk.Tk()
        JanelaRelatorios(relatorios_root)
        relatorios_root.mainloop()

    def limpar_campos_entrada(self):
        self.entry_numero_processo.delete(0, tk.END)
        self.entry_assunto.delete(0, tk.END)
        self.entry_data_criacao.delete(0, tk.END)
        self.entry_setor_responsavel.delete(0, tk.END)
        self.combo_status.current(0)
        self.text_descricao.delete("1.0", tk.END)
        self.entry_numero_processo.focus()

        if self.tree_processos.selection():
            self.tree_processos.selection_remove(self.tree_processos.selection()[0])

        self.id_selecionado = None
        self.btn_salvar_edicao.config(state="disabled")
        self.btn_excluir.config(state="disabled")
        self.btn_cadastrar.config(state="normal")

    def carregar_processos_na_treeview(self):
        for i in self.tree_processos.get_children():
            self.tree_processos.delete(i)
        try:
            processos = get_all_processos()
            for proc in processos:
                self.tree_processos.insert("", tk.END, values=proc)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar processos: {e}")

    def ao_selecionar_processo(self, event):
        selecionado_item_id = self.tree_processos.focus()
        if not selecionado_item_id:
            self.limpar_campos_entrada()
            return

        valores = self.tree_processos.item(selecionado_item_id, "values")
        self.limpar_campos_entrada()

        self.id_selecionado = valores[0]
        self.entry_numero_processo.insert(0, valores[1])
        self.entry_assunto.insert(0, valores[2])
        self.entry_data_criacao.insert(0, valores[3])
        self.entry_setor_responsavel.insert(0, valores[4])
        self.combo_status.set(valores[5])

        try:
            processo_completo = get_processo_by_id(self.id_selecionado)
            if processo_completo and processo_completo[6] is not None:
                self.text_descricao.insert("1.0", processo_completo[6])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar descrição: {e}")

        self.btn_salvar_edicao.config(state="normal")
        self.btn_excluir.config(state="normal")
        self.btn_cadastrar.config(state="disabled")

    def cadastrar_processo(self):
        num_proc = self.entry_numero_processo.get().strip()
        assunto = self.entry_assunto.get().strip()
        data_criacao = self.entry_data_criacao.get().strip()
        setor = self.entry_setor_responsavel.get().strip()
        status = self.combo_status.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()

        if not all([num_proc, assunto, data_criacao, setor, status]):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            if add_processo(num_proc, assunto, data_criacao, setor, status, descricao):
                messagebox.showinfo("Sucesso", "Processo cadastrado.")
                self.limpar_campos_entrada()
                self.carregar_processos_na_treeview()
            else:
                messagebox.showerror("Erro", "Número de processo já existe.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    def salvar_edicao_processo(self):
        if self.id_selecionado is None:
            return

        num_proc = self.entry_numero_processo.get().strip()
        assunto = self.entry_assunto.get().strip()
        data_criacao = self.entry_data_criacao.get().strip()
        setor = self.entry_setor_responsavel.get().strip()
        status = self.combo_status.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()

        if not all([num_proc, assunto, data_criacao, setor, status]):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            if update_processo(self.id_selecionado, num_proc, assunto, data_criacao, setor, status, descricao):
                messagebox.showinfo("Sucesso", "Processo atualizado.")
                self.limpar_campos_entrada()
                self.carregar_processos_na_treeview()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar processo.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def excluir_processo_selecionado(self):
        if self.id_selecionado is None:
            return

        confirm = messagebox.askyesno("Confirmação", "Deseja excluir o processo?")
        if not confirm:
            return

        try:
            if delete_processo(self.id_selecionado):
                messagebox.showinfo("Sucesso", "Processo excluído.")
                self.limpar_campos_entrada()
                self.carregar_processos_na_treeview()
            else:
                messagebox.showerror("Erro", "Erro ao excluir processo.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaGestao(root)
    root.mainloop()
