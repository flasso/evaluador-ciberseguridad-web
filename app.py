from flask import Flask, render_template, request

app = Flask(__name__)

# Opciones estándar
opciones = ['Sí', 'No', 'Parcialmente', 'No sé']

# Definición de las preguntas agrupadas
preguntas = {
    "Gestión y visibilidad": [
        ("responsable_seguridad", "¿Tu empresa cuenta con un responsable formal de seguridad de la información?"),
        ("monitoreo_seguridad", "¿Se realiza monitoreo regular de eventos de seguridad?"),
        ("inventario_activos", "¿Tienes un inventario actualizado de activos (equipos, datos, software)?"),
    ],
    "Protección de red y perímetro": [
        ("firewall", "¿Tu empresa cuenta con un firewall de red?"),
        ("revision_firewall", "¿El firewall es revisado y configurado periódicamente?"),
        ("wifi_segura", "¿Tu red Wi-Fi está segura y separada de invitados?"),
    ],
    "Protección de dispositivos y datos": [
        ("antivirus", "¿Todos los equipos cuentan con antivirus con EDR actualizado?"),
        ("actualizaciones", "¿Los sistemas operativos se actualizan regularmente?"),
        ("contraseñas", "¿Las contraseñas son fuertes y únicas?"),
        ("mfa", "¿Se usa autenticación multifactor (MFA) en cuentas críticas?"),
    ],
    "Respaldo y recuperación": [
        ("backups_frecuencia", "¿Las copias de seguridad son diarias o frecuentes?"),
        ("backups_prueba", "¿Las copias de seguridad se prueban periódicamente?"),
        ("backups_offline", "¿Tienes copias de seguridad offline o inmutables?"),
    ],
    "Concientización y respuesta": [
        ("capacitacion", "¿El personal recibe capacitación regular en ciberseguridad?"),
        ("plan_incidentes", "¿Existe un plan documentado de respuesta a incidentes?"),
        ("reporte_incidentes", "¿Los empleados saben cómo reportar incidentes?"),
    ]
}

# Puntuación por respuesta
puntos = {
    "Sí": 3,
    "Parcialmente": 1,
    "No": 0,
    "No sé": 0
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {}
        puntaje_obtenido = 0
        maximo = 0

        for grupo, lista in preguntas.items():
            for campo, texto in lista:
                resp = request.form.get(campo, "No sé")
                respuestas[texto] = resp
                puntaje_obtenido += puntos.get(resp, 0)
                maximo += 3

        porcentaje = round((puntaje_obtenido / maximo) * 100)

        # Tabla de referencia
        if porcentaje >= 81:
            categoria = "Postura robusta"
            recomendacion = "¡Felicidades! Mantén las buenas prácticas y revisa periódicamente."
        elif porcentaje >= 61:
            categoria = "Buena base"
            recomendacion = "Bien, pero puedes mejorar puntos clave para subir al siguiente nivel."
        elif porcentaje >= 31:
            categoria = "Riesgo elevado"
            recomendacion = "Debes priorizar las áreas débiles y fortalecer tus controles."
        else:
            categoria = "Riesgo crítico"
            recomendacion = "Actúa de inmediato: tu empresa es muy vulnerable."

        return render_template(
            "resultados.html",
            respuestas=respuestas,
            porcentaje=porcentaje,
            categoria=categoria,
            recomendacion=recomendacion
        )

    return render_template("index.html", preguntas=preguntas, opciones=opciones)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
