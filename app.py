from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Utilizan herramientas de monitoreo del estado de los equipos?", ["Sí, monitoreo continuo", "Sí, revisión manual", "Parcial", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "Personal no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen Antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "Personal no especializado", "Nadie asignado", "No se hace"]),
    ]),
    ("Gestión Remota y Respuesta", [
        ("¿Cómo gestionan de forma remota los equipos?", ["Herramienta RMM", "TeamViewer/AnyDesk", "Visitas presenciales", "No se gestionan"]),
        ("¿Tienen un plan definido de respuesta ante incidentes como ransomware?", ["Sí, documentado y probado", "Sí, pero no probado", "Solo informal", "No existe"]),
    ])
]

ponderacion = {
    "¿Respaldan datos críticos a diario?": 3,
    "¿Prueban restauración de respaldos?": 3,
    "¿Capacita regularmente a sus empleados en ciberseguridad?": 3,
    "¿Tienen Antivirus con EDR en todos los equipos?": 3,
    "¿Actualizan el sistema operativo y software con parches recientes?": 3,
    "¿Tienen un plan definido de respuesta ante incidentes como ransomware?": 3,
}

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = request.form.to_dict()
        nombre = respuestas.pop("nombre", "")
        correo = respuestas.pop("correo", "")
        empresa = respuestas.pop("empresa", "")
        sector = respuestas.pop("sector", "")
        pcs = respuestas.pop("pcs", "")
        total = 0
        puntos = 0
        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                valor = respuestas.get(pregunta)
                if valor is not None:
                    max_p = ponderacion.get(pregunta, 1) * 3
                    total += max_p
                    puntos += (3 - opciones.index(valor)) * ponderacion.get(pregunta, 1)
        porcentaje = round((puntos / total) * 100, 2) if total else 0

        # Email
        cuerpo = f"""Empresa: {empresa}
Nombre: {nombre}
Correo: {correo}
Sector: {sector}
Núm. PCs: {pcs}
Postura: {porcentaje}%
"""
        for k, v in respuestas.items():
            cuerpo += f"{k}: {v}\n"

        msg = Message("Resultado evaluación ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas, segmentos=segmentos, porcentaje=porcentaje, empresa=empresa)

    return render_template("index.html", segmentos=segmentos)
