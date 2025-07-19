from flask import Flask, render_template, request

app = Flask(__name__)

# Definición de las preguntas segmentadas
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No seguro", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Actualizaciones de sistema/software son automáticas?", ["Sí, automatizadas", "Manual regular", "Irregular", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {}
        puntaje_total = 0
        total_preguntas = 0
        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                resp = request.form.get(pregunta)
                respuestas[pregunta] = resp
                # Asignamos puntaje (ejemplo: mejor respuesta = 4, peor = 1)
                if resp:
                    puntaje = 4 - opciones.index(resp)
                    puntaje_total += puntaje
                    total_preguntas += 1

        porcentaje = int((puntaje_total / (total_preguntas * 4)) * 100) if total_preguntas else 0

        return render_template(
            "resultados.html",
            respuestas=respuestas,
            porcentaje=porcentaje
        )

    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
sw