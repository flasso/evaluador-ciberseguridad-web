from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Datos de la Empresa", [
        ("Nombre de la empresa", [""]),
        ("Nombre del contacto", [""]),
        ("Correo electrónico", [""]),
        ("Sector", ["Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otros"]),
        ("Ciudad", [""]),
        ("País", ["Colombia"]),
        ("Número de equipos", ["1-50", "51-150", "151-300", "301-500", "Más de 500"])
    ]),
    ("Gestión y Planeación", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean regularmente el estado de los equipos?", ["Sí, diariamente", "Sí, semanalmente", "Ocasionalmente", "No"]),
        ("¿Cómo gestionan remotamente los equipos?", ["Software especializado", "Acceso remoto manual", "No gestionan", "No saben"]),
        ("¿Tienen plan de respuesta ante incidentes como ransomware?", ["Sí, documentado y probado", "Sí, pero informal", "No definido", "No saben"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"])
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y segmentada?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"])
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, política definida + gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"])
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"])
    ])
]

@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():
    if request.method == "POST":
        respuestas = request.form.to_dict()
        return render_template("resultados.html", respuestas=respuestas, segmentos=segmentos)
    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
