from flask import Flask, render_template, request

app = Flask(__name__)

# Tabla de referencia
REFERENCIA = [
    (0, 30, "RIESGO CRÍTICO", "Necesitas actuar de inmediato. Tu empresa es altamente vulnerable."),
    (31, 60, "RIESGO ELEVADO", "Hay muchas debilidades que debes corregir cuanto antes."),
    (61, 80, "BUENA BASE", "Tu postura es aceptable, pero con áreas de mejora."),
    (81, 100, "POSTURA ROBUSTA", "Excelente, sigue manteniendo y revisando periódicamente.")
]

# Definir las preguntas por grupo
PREGUNTAS = [
    {
        "grupo": "Datos de la Empresa",
        "preguntas": [
            {"id": "empresa", "texto": "Nombre de la empresa", "tipo": "text"},
            {"id": "contacto", "texto": "Nombre del contacto", "tipo": "text"},
            {"id": "email", "texto": "Correo electrónico", "tipo": "email"},
            {"id": "sector", "texto": "Sector", "tipo": "select", "opciones": ["Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otros"]},
            {"id": "ciudad", "texto": "Ciudad", "tipo": "text"},
            {"id": "pais", "texto": "País", "tipo": "text", "valor": "Colombia"}
        ]
    },
    {
        "grupo": "Gestión y Visibilidad",
        "preguntas": [
            {"id": "responsable", "texto": "¿Hay un responsable claro de TI?", "opciones": ["Sí, dedicado", "Sí, parcial", "Externo", "No"]},
            {"id": "monitoreo", "texto": "¿Se monitorean los eventos de seguridad?", "opciones": ["Diario", "Semanal", "Solo cuando hay problemas", "No"]}
        ]
    },
    {
        "grupo": "Protección de Red",
        "preguntas": [
            {"id": "firewall", "texto": "¿Cuenta con un firewall de hardware o UTM?", "opciones": ["Sí, bien gestionado", "Sí, pero no bien gestionado", "No tiene", "No sabe"]},
            {"id": "wifi", "texto": "¿La red Wi-Fi está segura (WPA2/WPA3, separada para invitados)?", "opciones": ["Sí", "Parcial", "No", "No sabe"]}
        ]
    },
    {
        "grupo": "Protección de Dispositivos y Datos",
        "preguntas": [
            {"id": "antivirus", "texto": "¿Todos los equipos tienen antivirus con EDR?", "opciones": ["Sí, todos", "La mayoría", "Gratis o básicos", "No"]},
            {"id": "actualizaciones", "texto": "¿Las actualizaciones son automáticas y regulares?", "opciones": ["Sí, automatizado", "Manual, regular", "Ocasional", "No"]}
        ]
    },
    {
        "grupo": "Respaldo y Continuidad",
        "preguntas": [
            {"id": "backup", "texto": "¿Realizan copias de seguridad diarias y probadas?", "opciones": ["Sí, diario", "Semanal", "Mensual", "No"]},
            {"id": "plan", "texto": "¿Tienen plan documentado de respuesta a incidentes?", "opciones": ["Sí, probado", "Sí, sin probar", "No", "No sabe"]}
        ]
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = dict(request.form)
        puntuacion = 0
        maximo = 0
        recomendaciones = []

        # Calcular puntuación (5, 3, 1, 0)
        for grupo in PREGUNTAS[1:]:  # Saltar encabezado
            for preg in grupo["preguntas"]:
                resp = respuestas.get(preg["id"], "")
                if resp.startswith("Sí"):
                    puntos = 5
                elif resp in ["Parcial", "Semanal", "Manual, regular", "La mayoría", "Sí, sin probar"]:
                    puntos = 3
                elif resp in ["Solo cuando hay problemas", "Gratis o básicos", "Mensual", "No sabe"]:
                    puntos = 1
                else:
                    puntos = 0
                puntuacion += puntos
                maximo += 5

        porcentaje = int((puntuacion / maximo) * 100) if maximo > 0 else 0

        concepto = ""
        for minimo, maximo_rango, postura, mensaje in REFERENCIA:
            if minimo <= porcentaje <= maximo_rango:
                concepto = f"{postura}: {mensaje}"

        if porcentaje <= 60:
            recomendaciones.append("Te recomendamos contactar a un especialista en ciberseguridad para diseñar un plan de mejora.")
        else:
            recomendaciones.append("Sigue revisando y mejorando continuamente tus prácticas de seguridad.")

        return render_template("resultados.html",
                               respuestas=respuestas,
                               porcentaje=porcentaje,
                               concepto=concepto,
                               recomendaciones=recomendaciones)

    return render_template("index.html", preguntas=PREGUNTAS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
