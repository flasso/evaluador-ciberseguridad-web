from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = {
    "Gestión y Visibilidad": [
        ("¿Quién es el responsable de TI y ciberseguridad?", ["Dedicado y certificado", "Personal administrativo", "Proveedor externo", "Nadie"]),
        ("¿Hay monitoreo regular de seguridad?", ["Diario", "Semanal", "Solo ante incidentes", "No"]),
        ("¿Existe inventario actualizado de activos?", ["Sí, detallado", "Parcial", "No actualizado", "No"])
    ],
    "Protección de Red": [
        ("¿Tienen firewall de hardware?", ["Sí, bien configurado", "Sí, pero mal configurado", "Solo software en PC", "No"]),
        ("¿Quién gestiona el firewall?", ["Especialista en seguridad", "TI interno no dedicado", "Proveedor general", "No se gestiona"]),
        ("¿Wi-Fi está separado y seguro?", ["Sí, WPA3 y redes separadas", "Solo una red segura", "No seguro", "No sé"])
    ],
    "Protección de Dispositivos": [
        ("¿Todos tienen antivirus con EDR?", ["Sí, empresarial en todos", "En la mayoría", "Gratuitos", "No"]),
        ("¿Actualizaciones automáticas activas?", ["Sí, automatizadas", "Sí, manuales", "Irregulares", "No"]),
        ("¿Política de contraseñas fuertes?", ["Sí, con gestor", "Inconsistente", "No clara", "No"]),
        ("¿MFA activado en cuentas críticas?", ["Sí en todas", "En algunas", "Pocas", "Ninguna"])
    ],
    "Respaldo y Continuidad": [
        ("¿Backups diarios de datos críticos?", ["Sí, diarios", "Semanales", "Mensuales", "Nunca"]),
        ("¿Prueban restaurar backups?", ["Sí, documentado", "Ocasional", "Nunca", "No sé"]),
        ("¿Backups offline/inmutables?", ["Sí", "No", "No sé", "Desconozco"]),
        ("¿Plan de continuidad del negocio?", ["Sí, probado", "Documentado sin probar", "Idea básica", "No"])
    ],
    "Concienciación y Respuesta": [
        ("¿Capacitación regular a empleados?", ["Sí, anual", "Ocasional", "Nunca", "No sé"]),
        ("¿Procedimiento de reporte de incidentes?", ["Sí, claro", "Verbal", "No existe", "No sé"]),
        ("¿Plan de respuesta a incidentes?", ["Sí, probado", "Documentado", "Básico", "No"])
    ]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = dict(request.form)
        return render_template("resultados.html", respuestas=respuestas)
    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

