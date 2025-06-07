# 🗂️ Gestão de Processos Administrativos Internos

Sistema em Python para gerenciar processos administrativos internos, com funcionalidades de login, cadastro de processos e geração de relatórios.

## 📌 Funcionalidades

- 🔐 Autenticação de usuários
- 📝 Cadastro e gerenciamento de processos administrativos
- 📊 Geração de relatórios
- 💾 Armazenamento local com SQLite

## 🛠️ Tecnologias Utilizadas

- Python 
- SQLite

## 📦 Instalação

1. Clone o repositório:

   `bash
   git clone https://github.com/JoaoLua/Gest-o-de-Processos-Administrativos-Internos.git
   cd Gest-o-de-Processos-Administrativos-Internos


Acesse a pasta raiz do projeto:

bash
Copiar código
cd gestao_processos
Execute o sistema de login:

bash
Copiar código
python -m gui.app_login
📁 Estrutura do Projeto
pgsql
Copiar código
gestao_processos/
│
├── gui/
│   ├── app_login.py
│   ├── app_gestao.py
│   └── app_relatorios.py
│
├── data/
│   └── banco.db
│
├── database/
│   └── database.py
│
├── init.py
└── README.md
