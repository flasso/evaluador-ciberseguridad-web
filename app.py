from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        sector = request.form.get("sector")
        empleados = request.form.get("empleados")
        gestion_ti = request.form.get("gestion_ti")
        # Aquí puedes agregar la lógica para calcular resultados y recomendaciones
        return render_template(
            "informe.html",
            nombre=nombre,
            sector=sector,
            empleados=empleados,
            gestion_ti=gestion_ti
        )
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

