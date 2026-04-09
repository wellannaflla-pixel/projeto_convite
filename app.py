import os
from flask import Flask, render_template, request, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

# Aqui você define o login e a senha que vai usar para entrar
USER_DATA = {
    "admin": "14162227"  # Você pode mudar "1234" para a senha que quiser
}

@auth.verify_password
def verify(username, password):
    if username in USER_DATA and USER_DATA[username] == password:
        return username

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'presencas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela de convidados
class Convidado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    acompanhantes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Convidado {self.nome}>'

# Rota principal (Formulário)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        qtd = request.form.get('quantidade')
        
        if nome and qtd:
            novo_convidado = Convidado(nome=nome, acompanhantes=int(qtd))
            db.session.add(novo_convidado)
            db.session.commit()
            return redirect(url_for('sucesso'))
    
    # ESTA LINHA ABAIXO É A QUE FALTAVA:
    # Ela precisa estar fora do "if" para que o formulário apareça ao abrir o site
    return render_template('index.html')

@app.route('/sucesso')
def sucesso():
    return "<h1>Presença confirmada! Obrigado.</h1>"
@app.route('/admin')

@app.route('/admin')
@auth.login_required  # <--- ESSA É A LINHA QUE BLOQUEIA A ENTRADA
def admin():
    # Busca todos os convidados no banco de dados
    todos_convidados = Convidado.query.all()
    
    # Soma o total de pessoas
    total_pessoas = sum([c.acompanhantes + 1 for c in todos_convidados])
    
    return render_template('admin.html', convidados=todos_convidados, total=total_pessoas)

def admin():
    # Busca todos os convidados no banco de dados
    todos_convidados = Convidado.query.all()
    
    # Soma o total de pessoas (convidado + acompanhantes)
    total_pessoas = sum([c.acompanhantes + 1 for c in todos_convidados])
    
    return render_template('admin.html', convidados=todos_convidados, total=total_pessoas)

if __name__ == '__main__':
    # Isso garante que o banco seja criado no Render também
    with app.app_context():
        db.create_all()
    app.run()