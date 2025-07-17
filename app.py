from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecreto'  # Cambia esto por una clave más segura

# Las preguntas de ejemplo
PREGUNTAS = [
    {
        "texto": "¿Tienes un responsable claro de ciberseguridad?",
        "opciones": ["Sí, interno", "Sí, externo", "No"]
    },
    {
        "texto": "¿Tienes un firewall dedicado?",
        "opciones": ["Sí", "No", "No sé"]
    },
    {
        "texto": "¿Realizas backups regularmente?",
        "opciones": ["Diarios", "Semanales", "No"]
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["nombre"] = request.form["nombre"]
        session["empresa"] = request.form["empresa"]
        session["respuestas"] = {}
        return redirect(url_for("pregunta", num=0))
    return render_template("index.html")

@app.route("/pregunta/<int:num>", methods=["GET", "POST"])
def pregunta(num):
    if num >= len(PREGUNTAS):
        return redirect(url_for("resultado"))

    pregunta = PREGUNTAS[num]
    if request.method == "POST":
        respuesta = request.form["respuesta"]
        session["respuestas"][pregunta["texto"]] = respuesta
        session.modified = True
        return redirect(url_for("pregunta", num=num+1))
    return render_template("pregunta.html", num=num, pregunta=pregunta)

@app.route("/resultado")
def resultado():
    return render_template("resultado.html", respuestas=session.get("respuestas", {}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
