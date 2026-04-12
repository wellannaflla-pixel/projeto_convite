import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# SEGURANÇA
USER_DATA = {
    "admin": "14162227"
}

@auth.verify_password
def verify(username, password):
    if username in USER_DATA and USER_DATA[username] == password:
        return username
    return None

# BANCO DE DADOS
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'presencas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Convidado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    acompanhantes = db.Column(db.Integer, default=0)

# ROTAS
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        qtd = request.form.get('quantidade')
        if nome and qtd:
            novo = Convidado(nome=nome, acompanhantes=int(qtd))
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for('sucesso'))
    return render_template('index.html')

@app.route('/sucesso')
def sucesso():
    return "<h1>Presença confirmada!</h1>"

@app.route('/admin')
@auth.login_required
def admin():
    todos = Convidado.query.all()
    total = sum([c.acompanhantes + 1 for c in todos])
    return render_template('admin.html', convidados=todos, total=total)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/excluir/<int:id>')
@auth.login_required
def excluir(id):

convidado = Convidado.query.get_or_404(id)
    db.session.delete(convidado)
    db.session.commit()
    return redirect(url_for('admin'))