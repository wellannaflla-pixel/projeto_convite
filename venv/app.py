import os
from flask import Flask, render_template, request, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)

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
            
    return render_template('index.html')

@app.route('/sucesso')
def sucesso():
    return "<h1>Presença confirmada! Obrigado.</h1>"
@app.route('/admin')
def admin():
    # Busca todos os convidados no banco de dados
    todos_convidados = Convidado.query.all()
    
    # Soma o total de pessoas (convidado + acompanhantes)
    total_pessoas = sum([c.acompanhantes + 1 for c in todos_convidados])
    
    return render_template('admin.html', convidados=todos_convidados, total=total_pessoas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco de dados automaticamente
    app.run(debug=True)