import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuração de Segurança
USER_DATA = {
    "admin": "14162227"
}

@auth.verify_password
def verify(username, password):
    if username in USER_DATA and USER_DATA[username] == password:
        return username

# Configuração do Banco de Dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'presencas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela
class Convidado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    acompanhantes = db.Column(db.Integer, default=0)

# Rota Inicial
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
    return render_template('index.html')

# Rota Sucesso
@app.route('/sucesso')
def sucesso():
    return "<h1>Presença confirmada! Obrigado.</h1>"

# Rota Admin (PROTEGIDA)
@app.route('/admin')
@auth.login_required
def admin():
    todos_convidados = Convidado.query.all()
    total_pessoas = sum([c.acompanhantes + 1 for c in todos_convidados])
    return render_template('admin.html', convidados=todos_convidados, total=total_pessoas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)