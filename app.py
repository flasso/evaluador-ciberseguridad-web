from flask import Flask, render_template, request

app = Flask(__name__)

# Definimos las preguntas por sección
preguntas = {
    "Información General": [
        ("Nombre de la empresa", ""),
        ("Persona de contacto", ""),
        ("Correo electrónico", ""),
        ("Ciudad", ""),
        ("País", "Colombia"),
    ],
    "Infraestructura": [
        ("¿Tiene firewall de hardware o UTM?", ["Sí", "No", "No sé", "Solo software"]),
        ("¿Revisa regularmente la configuración del firewall?", ["Sí", "No", "No sé", "No tengo firewall"]),
        ("¿Tiene WiFi con WPA2/WPA3 y red de invitados separada?", ["Sí", "No", "No sé", "Solo red básica"]),
        ("¿Todos los equipos tienen antivirus con EDR?", ["Sí", "No", "No sé", "Solo en algunos equipos"]),
    ],
    "Gestión TI": [
        ("¿Cuenta con personal responsable de TI o seguridad?", ["Sí dedicado", "Sí parcial", "No", "Proveedor externo"]),
        ("¿Realizan copias de seguridad periódicas?", ["Sí diario", "Semanal", "Mensual", "No"]),
        ("¿Las copias son probadas y están offline/inmutables?", ["Sí", "No", "No sé", "Solo online"]),
    ],
    "Concienciación y Respuesta": [
        ("¿Capacitan a los empleados en ciberseguridad?", ["Sí anual", "Ocasional", "Nunca", "No sé"]),
        ("¿Tienen plan de respuesta a incidentes?", ["Sí probado", "Sí documentado", "Idea básica", "No"]),
    ]
}

# Ponderación por respuesta (orden: mejor a peor)
puntajes = [3, 2, 1, 0]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {}
        totales = {}
        max_puntos = {}
        for seccion, qs in preguntas.items():
            respuestas[seccion] = []
            totales[seccion] = 0
            max_puntos[seccion] = 0
            for i, (q, opciones) in enumerate(qs):
                clave = f"{seccion}_{i}"
                val = request.form.get(clave)
                if isinstance(opciones, list):
                    puntos = puntajes[opciones.index(val)] if val in opciones else 0
                    totales[seccion] += puntos
                    max_puntos[seccion] += max(puntajes)
                respuestas[seccion].append((q, val))

        # Calcular porcentajes por sección
        porcentajes = {
            seccion: round((totales[seccion]/max_puntos[seccion])*100) if max_puntos[seccion] > 0 else 0
            for seccion in preguntas.keys()
        }
        promedio_general = round(sum(porcentajes.values())/len(porcentajes))

        # Determinar concepto
        if promedio_general >= 80:
            concepto = "Su postura es BUENA. Mantenga las buenas prácticas y continúe mejorando."
        elif promedio_general >= 60:
            concepto = "Su postura es ACEPTABLE, pero con áreas de mejora. Tome acciones inmediatas."
        elif promedio_general >= 40:
            concepto = "Su postura es de RIESGO ELEVADO. Urge implementar medidas."
        else:
            concepto = "Su postura es CRÍTICA. Requiere intervención urgente de especialistas."

        return render_template("resultados.html", respuestas=respuestas, porcentajes=porcentajes,
                               promedio_general=promedio_general, concepto=concepto)

    return render_template("index.html", preguntas=preguntas)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

