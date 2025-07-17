from flask import Flask, render_template, request

app = Flask(__name__)

# Definición de las preguntas
PREGUNTAS = [
    {"id": "q1", "texto": "¿Utilizan herramientas de acceso remoto seguras (AnyDesk, TeamViewer con autenticación)?", "opciones": ["Siempre", "A veces", "Rara vez", "Nunca"]},
    {"id": "q2", "texto": "¿Todo el software instalado en los equipos es original y con licencia?", "opciones": ["Siempre", "Mayormente", "Parcialmente", "No"]},
    {"id": "q3", "texto": "¿Se actualizan regularmente los sistemas operativos de todos los dispositivos?", "opciones": ["Automáticamente", "Mensualmente", "Ocasionalmente", "Nunca"]},
    {"id": "q4", "texto": "¿Se realizan copias de seguridad de los datos críticos?", "opciones": ["Diariamente", "Semanalmente", "Mensualmente", "Nunca"]},
    {"id": "q5", "texto": "¿Existe un plan documentado de respuesta a incidentes?", "opciones": ["Sí, probado", "Sí, pero no probado", "En borrador", "No"]},
    {"id": "q6", "texto": "¿Todos los empleados reciben capacitación en ciberseguridad?", "opciones": ["Anualmente", "Ocasionalmente", "Rara vez", "Nunca"]},
    {"id": "q7", "texto": "¿Las redes Wi-Fi están protegidas con contraseñas fuertes y separadas para invitados?", "opciones": ["Sí, bien configuradas", "Solo contraseña", "Débil/no separada", "No estoy seguro"]},
    {"id": "q8", "texto": "¿Se usa autenticación multifactor (MFA) en cuentas críticas?", "opciones": ["En todas", "En algunas", "Muy pocas", "Ninguna"]},
    {"id": "q9", "texto": "¿Existen políticas claras sobre contraseñas fuertes?", "opciones": ["Sí y se aplican", "Sí, poco aplicadas", "Inconsistentes", "No"]},
    {"id": "q10", "texto": "¿Se revisan regularmente los registros de seguridad (firewall, antivirus)?", "opciones": ["Diariamente", "Semanalmente", "Mensualmente", "Nunca"]},
    {"id": "q11", "texto": "¿Tienen un inventario actualizado de activos digitales?", "opciones": ["Sí, completo", "Parcial", "Obsoleto", "No"]},
    {"id": "q12", "texto": "¿Las copias de seguridad se prueban periódicamente?", "opciones": ["Sí", "Rara vez", "No", "No hay backups"]},
    {"id": "q13", "texto": "¿Hay al menos una copia de seguridad aislada (offline/inmutable)?", "opciones": ["Sí", "No", "No estoy seguro", "No aplica"]},
    {"id": "q14", "texto": "¿Cuánto tiempo podrían operar tras un ataque antes de un impacto grave?", "opciones": [">1 semana", "3 días", "1 día", "<1 día"]}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        empresa = request.form.get("empresa")
        contacto = request.form.get("contacto")
        email = request.form.get("email")
        sector = request.form.get("sector")
        ciudad = request.form.get("ciudad")
        pais = request.form.get("pais")

        respuestas = {}
        puntaje = 0

        for pregunta in PREGUNTAS:
            r = request.form.get(pregunta["id"])
            respuestas[pregunta["texto"]] = r
            if r == pregunta["opciones"][0]:
                puntaje += 4
            elif r == pregunta["opciones"][1]:
                puntaje += 3
            elif r == pregunta["opciones"][2]:
                puntaje += 2
            else:
                puntaje += 1

        porcentaje = (puntaje / (len(PREGUNTAS) * 4)) * 100

        if porcentaje >= 80:
            postura = "Robusta"
            color = "green"
        elif porcentaje >= 60:
            postura = "Aceptable"
            color = "blue"
        elif porcentaje >= 40:
            postura = "Débil"
            color = "orange"
        else:
            postura = "Crítica"
            color = "red"

        return render_template("resultado.html",
                               empresa=empresa,
                               contacto=contacto,
                               email=email,
                               sector=sector,
                               ciudad=ciudad,
                               pais=pais,
                               respuestas=respuestas,
                               porcentaje=porcentaje,
                               postura=postura,
                               color=color)

    return render_template("cuestionario.html", preguntas=PREGUNTAS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
