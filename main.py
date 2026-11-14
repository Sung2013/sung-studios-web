from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Conecta o SQLAlchemy ao Flask
db = SQLAlchemy(app)


# Modelo das contas
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False,
        default="usuario"
    )


@app.route("/")
def hello():
    return render_template("hello.html")
@app.route("/cadastro")
def cadastro():
    if request.method == "POST":
        # pega os dados enviados pelo formulario
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        # verifica se o nome de usuario ja existe
        if User.query.filter_by(username=username).first():
            return "username ja esta em uso, tente outro", 400

        #verifica se o email ja existe
        if User.query.filter_by(email=email).first():
            return "email ja esta cadastrado, tente outro", 400

        # transforma a senha em hash
        senha_hash = generate_password_hash(senha)

        # cria o usuario
        user = User(username=username, email=email, senha=senha_hash, tipo="usuario")

        # salva no banco de dados
        db.session.add(user)
        db.session.commit()

        # volta para a pagina inicial
        return redirect(url_for("hello"))

    return render_template("cadastro.html")


# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)