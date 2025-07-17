from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SECTORES = [
    "Servicios", "Manufactura", "Tecnología", "Alimentos",
    "Legales", "Contables", "Distribución", "Otros"
]

PAIS_DEFECTO = "Colombia"

PREGUNTAS = [
    "¿La empresa cuenta con un firewall de hardware o UTM bien configurado?",
    "¿Se realizan respaldos diarios o frecuentes de los datos críticos?",
    "¿Existe un plan formal de respuesta a incidentes?",
    "¿Los empleados reciben capacitación regular en ciberseguridad?",
    "¿Se actualizan automáticamente los sistemas operativos y software?",
    "¿Se usa autenticación multifactor en servicios críticos?",
    "¿Existe un inventario actualizado de activos tecnológicos?",
    "¿Hay separación de redes WiFi para invitados y empresa?",
    "¿Las contraseñas siguen una política robusta y segura?",
    "¿Hay monitoreo constante de eventos de seguridad?",
    "¿Las copias de respaldo se prueban regularmente?",
    "¿Hay al menos una copia offline/inmutable para ransomware?",
    "¿Hay un responsable designado para la ciberseguridad?",
    "¿Se ha evaluado el impacto de una inoperatividad prolongada?"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        datos = {
            "empresa": request.form["empresa"],
            "contacto": request.form["contacto"],
            "email": request.form["email"],
            "sector": request.form["sector"],
            "ciudad": request.form["ciudad"],
            "pais": request.form["pais"]
        }
        return redirect(url_for("cuestionario", **datos))
    return render_template("index.html", sectores=SECTORES, pais_defecto=PAIS_DEFECTO)

@app.route("/cuestionario")
def cuestionario():
    datos = request.args
    return render_template("cuestionario.html", preguntas=PREGUNTAS, datos=datos)

@app.route("/resultados", methods=["POST"])
def resultados():
    respuestas = []
    puntaje = 0
    for i in range(len(PREGUNTAS)):
        respuesta = request.form.get(f"p{i}")
        respuestas.append(respuesta)
        if respuesta == "Sí":
            puntaje += 1

    porcentaje = (puntaje / len(PREGUNTAS)) * 100

    if porcentaje <= 30:
        postura = "Crítica"
        descripcion = "Tu postura de ciberseguridad es crítica, muy vulnerable a ataques. Se requiere acción inmediata."
    elif porcentaje <= 60:
        postura = "Débil"
        descripcion = "Tu empresa tiene debilidades importantes. Es necesario mejorar varias áreas clave."
    elif porcentaje <= 80:
        postura = "Aceptable"
        descripcion = "Tu empresa tiene una base aceptable, pero aún hay margen para fortalecer la seguridad."
    else:
        postura = "Robusta"
        descripcion = "Tu empresa tiene una postura robusta. Continúa vigilando y mejorando."

    return render_template("resultados.html",
                           respuestas=zip(PREGUNTAS, respuestas),
                           porcentaje=porcentaje,
                           postura=postura,
                           descripcion=descripcion)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

