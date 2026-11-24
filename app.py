import os
import time

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Render fornece DATABASE_URL (PostgreSQL). Sem ela, usa SQLite local.
db_url = os.getenv("DATABASE_URL", "sqlite:///tarefas.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "concluida": self.concluida}


def iniciar_banco(tentativas=10):
    """Cria as tabelas, aguardando o banco ficar disponível."""
    for _ in range(tentativas):
        try:
            with app.app_context():
                db.create_all()
            return
        except OperationalError:
            time.sleep(2)
    raise RuntimeError("Não foi possível conectar ao banco de dados.")


iniciar_banco()


# ---------- Interface web ----------
@app.route("/")
def index():
    tarefas = Tarefa.query.order_by(Tarefa.id.desc()).all()
    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()
    if titulo:
        db.session.add(Tarefa(titulo=titulo))
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/concluir/<int:id>", methods=["POST"])
def concluir(id):
    tarefa = db.get_or_404(Tarefa, id)
    tarefa.concluida = not tarefa.concluida
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarefa = db.get_or_404(Tarefa, id)
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if titulo:
            tarefa.titulo = titulo
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("editar.html", tarefa=tarefa)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    tarefa = db.get_or_404(Tarefa, id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("index"))


# ---------- API JSON ----------
@app.route("/api/tarefas")
def api_listar():
    return jsonify([t.to_dict() for t in Tarefa.query.order_by(Tarefa.id).all()])


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
