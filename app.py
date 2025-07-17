from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Preguntas y opciones
PREGUNTAS = [
    {
        "id": "anydesk",
        "texto": "¿Tu empresa utiliza herramientas de acceso remoto seguras (como AnyDesk o TeamViewer) para soporte?",
        "opciones": ["Sí, siempre", "Sí, a veces", "No", "No estoy seguro"]
    },
    {
        "id": "software_original",
        "texto": "¿Todo el software en los equipos de tu empresa es original y con licencias válidas?",
        "opciones": ["Sí, todo", "La mayoría", "Muy poco", "Nada"]
    },
    {
        "id": "actualizaciones",
        "texto": "¿Los sistemas operativos y programas reciben actualizaciones periódicas?",
        "opciones": ["Automáticamente", "Manual pero regular", "Muy ocasionalmente", "Nunca"]
    },
    {
        "id": "politica_seguridad",
        "texto": "¿Tu empresa tiene una política de seguridad formal escrita?",
        "opciones": ["Sí y la seguimos", "Sí pero no se aplica bien", "No formal", "No existe"]
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        datos = {
            "empresa": request.form.get("empresa"),
            "contacto": request.form.get("contacto"),
            "email": request.form.get("email"),
            "sector": request.form.get("sector"),
            "ciudad": request.form.get("ciudad"),
            "pais": request.form.get("pais")
        }
        return redirect(url_for("cuestionario", **datos))
    return render_template("index.html")

@app.route("/cuestionario")
def cuestionario():
    datos = request.args
    return render_template("cuestionario.html", datos=datos, preguntas=PREGUNTAS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




