from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "evaluador2025"

# Definimos las preguntas y módulos aquí (simplificado, pero ya listo para ti)
modulos = [
    {
        "titulo": "Gestión y Visibilidad",
        "preguntas": [
            {
                "id": "q_responsable",
                "texto": "¿Quién es responsable de la ciberseguridad?",
                "opciones": [
                    ("Equipo dedicado", 5),
                    ("Personal TI parcial", 3),
                    ("Proveedor externo", 4),
                    ("Nadie", 0)
                ]
            },
            {
                "id": "q_monitoreo",
                "texto": "¿Se realiza monitoreo regular?",
                "opciones": [
                    ("Diario", 5),
                    ("Semanal", 3),
                    ("Nunca", 0)
                ]
            }
        ]
    },
    {
        "titulo": "Protección de Red",
        "preguntas": [
            {
                "id": "q_firewall",
                "texto": "¿Cuenta con firewall dedicado?",
                "opciones": [
                    ("Sí, bien configurado", 5),
                    ("Sí, pero no seguro", 2),
                    ("No", 0)
                ]
            }
        ]
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["nombre"] = request.form["nombre"]
        session["sector"] = request.form["sector"]
        session["tamano"] = request.form["tamano"]
        session["respuestas"] = {}
        session["puntaje"] = 0
        return redirect(url_for("preguntas", modulo_idx=0))
    return render_template("index.html")

@app.route("/preguntas/<int:modulo_idx>", methods=["GET", "POST"])
def preguntas(modulo_idx):
    if modulo_idx >= len(modulos):
        return redirect(url_for("resultado"))

    modulo = modulos[modulo_idx]

    if request.method == "POST":
        for pregunta in modulo["preguntas"]:
            respuesta = request.form.get(pregunta["id"])
            puntos = int(respuesta)
            session["respuestas"][pregunta["id"]] = puntos
            session["puntaje"] += puntos
        return redirect(url_for("preguntas", modulo_idx=modulo_idx+1))

    return render_template("preguntas.html", modulo=modulo, modulo_idx=modulo_idx)

@app.route("/resultado")
def resultado():
    puntaje = session.get("puntaje", 0)
    if puntaje <= 5:
        categoria = "RIESGO CRÍTICO"
        color = "red"
    elif puntaje <= 10:
        categoria = "RIESGO ELEVADO"
        color = "orange"
    elif puntaje <= 15:
        categoria = "BUENA BASE"
        color = "blue"
    else:
        categoria = "POSTURA ROBUSTA"
        color = "green"
    return render_template("resultado.html", puntaje=puntaje, categoria=categoria, color=color, nombre=session.get("nombre"))

import os

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
