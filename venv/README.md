📑 Sistema de Confirmação de Presença (Flask)
Este é um projeto Full Stack desenvolvido para gerenciar confirmações de presença em eventos. O sistema permite que convidados confirmem sua participação através de um formulário web, enquanto o organizador pode monitorar a lista de confirmados e o total de pessoas através de um painel administrativo.

🚀 Funcionalidades
Formulário de Inscrição: Captura o nome do convidado e o número de acompanhantes.

Banco de Dados: Armazenamento persistente utilizando SQLite e Flask-SQLAlchemy.

Painel Administrativo: Rota exclusiva /admin que lista todos os convidados e calcula automaticamente o total de pessoas confirmadas.

Design Responsivo: (Se você aplicou CSS) Interface amigável para acesso via celular.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.14

Framework Web: Flask

ORM (Banco de Dados): Flask-SQLAlchemy (SQLite)

Servidor de Produção: Gunicorn

Deploy: Render.com

## 📂 Estrutura do Projeto

Aqui está a organização dos arquivos do projeto:

```plaintext
projeto_convite/
├── app.py              # Lógica principal do servidor e rotas
├── requirements.txt    # Lista de dependências para o deploy
├── .gitignore          # Arquivos ignorados pelo Git (venv, db, etc)
├── templates/          # Arquivos HTML
│   ├── index.html      # Página do formulário
│   └── admin.html      # Painel de controle
└── static/             # (Opcional) Arquivos CSS/JS

⚙️ Como rodar o projeto localmente
Clone o repositório:

Bash
git clone https://github.com/SEU_USUARIO/projeto_convite.git
cd projeto_convite
Crie e ative o ambiente virtual:

Bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Execute a aplicação:

Bash
python app.py
Acesse: http://127.0.0.1:5000

🌐 Deploy
O projeto está configurado para deploy automático no Render. O banco de dados SQLite é gerado automaticamente na primeira execução através do contexto da aplicação (db.create_all()).

✍️ Autor
Wellington Silva de Jesus Rodrigues Estudante de Desenvolvimento Full Stack
