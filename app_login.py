import tkinter as tk
from tkinter import messagebox
from database import inicializar_banco, cadastrar_usuario, verificar_login
from app_gestao import JanelaGestao

class Login_cadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Acesso")
        self.root.geometry("600x400")  # Tamanho fixo da janela

        self.login_frame = tk.Frame(root)
        self.cadastro_frame = tk.Frame(root)

        self.create_login_screen()
        self.create_cadastro_screen()

        self.show_login_screen()

    def clear_entries(self, frame):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

    def show_login_screen(self):
        self.cadastro_frame.pack_forget()
        self.login_frame.pack(expand=True)
        self.clear_entries(self.login_frame)

    def show_cadastro_screen(self):
        self.login_frame.pack_forget()
        self.cadastro_frame.pack(expand=True)
        self.clear_entries(self.cadastro_frame)

    def create_login_screen(self):
        self.login_frame.config(padx=20, pady=20)
        tk.Label(self.login_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)

        # Campo de Email
        tk.Label(self.login_frame, text="Email:").pack(anchor="w", pady=(5, 0))
        self.email_login_entry = tk.Entry(self.login_frame, width=40)
        self.email_login_entry.pack(pady=5)

        # Campo de Senha
        tk.Label(self.login_frame, text="Senha:").pack(anchor="w", pady=(5, 0))
        self.senha_login_entry = tk.Entry(self.login_frame, show="*", width=40)
        self.senha_login_entry.pack(pady=5)

        # Botão de Login
        tk.Button(self.login_frame, text="Entrar", command=self.handle_login, width=15).pack(pady=10)

        # Botão para Cadastrar
        tk.Button(self.login_frame, text="Não tem conta? Cadastre-se", command=self.show_cadastro_screen, width=25).pack(pady=5)

    def create_cadastro_screen(self):
        self.cadastro_frame.config(padx=20, pady=20) # Adiciona padding ao frame

        tk.Label(self.cadastro_frame, text="Cadastro", font=("Arial", 18, "bold")).pack(pady=10)

        # Campo de Nome
        tk.Label(self.cadastro_frame, text="Nome:").pack(anchor="w", pady=(5, 0))
        self.nome_cadastro_entry = tk.Entry(self.cadastro_frame, width=40)
        self.nome_cadastro_entry.pack(pady=5)

        # Campo de Email
        tk.Label(self.cadastro_frame, text="Email:").pack(anchor="w", pady=(5, 0))
        self.email_cadastro_entry = tk.Entry(self.cadastro_frame, width=40)
        self.email_cadastro_entry.pack(pady=5)

        # Campo de Senha
        tk.Label(self.cadastro_frame, text="Senha:").pack(anchor="w", pady=(5, 0))
        self.senha_cadastro_entry = tk.Entry(self.cadastro_frame, show="*", width=40)
        self.senha_cadastro_entry.pack(pady=5)

        tk.Button(self.cadastro_frame, text="Cadastrar", command=self.handle_cadastro, width=15).pack(pady=10)
        tk.Button(self.cadastro_frame, text="Voltar para Login", command=self.show_login_screen, width=20).pack(pady=5)

    def handle_login(self):
        email = self.email_login_entry.get()
        senha = self.senha_login_entry.get()

        if not email or not senha:
            messagebox.showwarning("Erro de Login", "Por favor, preencha todos os campos.")
            return

        usuario = verificar_login(email, senha)

        if usuario:
            messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {usuario[1]}!") 
            self.clear_entries(self.login_frame)
            self.root.destroy()
            gestao_root_tk = tk.Tk()
            app_gestao = JanelaGestao(gestao_root_tk)
            gestao_root_tk.mainloop()

        else:
            messagebox.showerror("Erro de Login", "Email ou senha incorretos.")

    def handle_cadastro(self):
        nome = self.nome_cadastro_entry.get()
        email = self.email_cadastro_entry.get()
        senha = self.senha_cadastro_entry.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Erro de Cadastro", "Por favor, preencha todos os campos.")
            return

        sucesso = cadastrar_usuario(nome, email, senha)

        if sucesso:
            messagebox.showinfo("Cadastro Bem-Sucedido", f"Usuário {nome} cadastrado com sucesso!")
            self.clear_entries(self.cadastro_frame)
            self.show_login_screen()
        else:
            messagebox.showerror("Erro de Cadastro", "Email já está cadastrado.")

if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    app = Login_cadastro(root)
    root.mainloop()