from flask import Flask, render_template, request

app = Flask(__name__)

# Tabla de referencia
REFERENCIA = [
    (0, 30, "RIESGO CRÍTICO", "Actúa de inmediato. La empresa es altamente vulnerable."),
    (31, 60, "RIESGO ALTO", "Existen brechas importantes que debes corregir."),
    (61, 80, "BUENA BASE", "Hay buenas prácticas, pero aún puedes mejorar."),
    (81, 100, "POSTURA ROBUSTA", "Excelente. Mantén y revisa periódicamente.")
]

# Grupos y preguntas
GRUPOS = [
    ("Datos de la Empresa", [
        ("empresa", "Nombre de la empresa"),
        ("contacto", "Nombre del contacto"),
        ("email", "Correo electrónico"),
        ("sector", "Sector", ["Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otros"]),
        ("ciudad", "Ciudad"),
        ("pais", "País", ["Colombia", "Otro"])
    ]),
    ("Gestión y Visibilidad", [
        ("responsable", "¿Tienes un responsable de TI?", ["Sí, dedicado", "Sí, parcial", "Externo", "No"]),
        ("monitoreo", "¿Se monitorean eventos de seguridad?", ["Sí, diario", "Sí, semanal", "Solo cuando hay problemas", "No"]),
        ("inventario", "¿Existe un inventario actualizado de equipos y datos?", ["Sí, completo", "Sí, parcial", "No", "No sabe"])
    ]),
    ("Protección de Red", [
        ("firewall", "¿Cuentas con un firewall de hardware/UTM?", ["Sí, bien gestionado", "Sí, mal gestionado", "No", "No sabe"]),
        ("wifi", "¿La red Wi-Fi está segura (WPA2/WPA3, separada para invitados)?", ["Sí", "Parcial", "No", "No sabe"])
    ]),
    ("Protección de Dispositivos y Datos", [
        ("antivirus", "¿Tienen antivirus con EDR?", ["Sí, todos", "La mayoría", "Gratis o básico", "No"]),
        ("actualizaciones", "¿Las actualizaciones son automáticas?", ["Sí, automatizadas", "Manual y regular", "Ocasional", "No"]),
        ("mfa", "¿Usan autenticación multifactor (MFA)?", ["Sí, en todas", "En algunas", "No", "No sabe"])
    ]),
    ("Respaldo y Continuidad", [
        ("backups", "¿Hacen backups diarios y probados?", ["Sí, diario y probado", "Semanal", "Mensual", "No"]),
        ("plan", "¿Tienen plan documentado de respuesta a incidentes?", ["Sí, probado", "Sí, sin probar", "No", "No sabe"])
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = dict(request.form)
        puntaje, maximo = 0, 0

        respuestas = {}
        for grupo, preguntas in GRUPOS[1:]:
            for p in preguntas:
                val = data.get(p[0], "")
                respuestas[p[1]] = val
                if val.startswith("Sí"):
                    puntaje += 5
                elif val in ["Parcial", "Semanal", "Manual y regular", "La mayoría", "Sí, sin probar"]:
                    puntaje += 3
                elif val in ["Solo cuando hay problemas", "Gratis o básico", "Mensual", "No sabe"]:
                    puntaje += 1
                else:
                    puntaje += 0
                maximo += 5

        porcentaje = int(puntaje / maximo * 100)
        postura = next((desc for minv, maxv, _, desc in REFERENCIA if minv <= porcentaje <= maxv), "")
        concepto = next((name for minv, maxv, name, _ in REFERENCIA if minv <= porcentaje <= maxv), "")

        recomendaciones = []
        if porcentaje <= 60:
            recomendaciones.append("Contrata un especialista para reforzar tu postura de ciberseguridad.")
        recomendaciones.append("Revisa las áreas más débiles e implementa las mejores prácticas.")
        recomendaciones.append("Evalúa periódicamente tu seguridad para mantenerla actualizada.")

        return render_template("resultados.html", data=data, respuestas=respuestas,
                               porcentaje=porcentaje, concepto=concepto, postura=postura,
                               referencia=REFERENCIA, recomendaciones=recomendaciones)
    return render_template("index.html", grupos=GRUPOS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
