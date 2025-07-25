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
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Utilizan herramientas de monitoreo?", ["Sí, 24/7", "Sí, periódicamente", "Ocasional", "No"]),
        ("¿Cómo gestionan remotamente los equipos?", ["Con herramientas seguras", "Por acceso directo", "Solo presencial", "No gestionan"]),
        ("¿Tienen un plan de respuesta ante incidentes?", ["Sí, formal y probado", "Sí, sin pruebas", "En desarrollo", "No"]),
    ]),
    ("Protección y Continuidad", [
        ("¿Tienen Firewall/UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo firewall software", "No firewall"]),
        ("¿Wi-Fi está segura y segmentada?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
        ("¿Antivirus con EDR?", ["Sí, EDR", "Sí, antivirus básico", "Antivirus gratuito", "No"]),
        ("¿MFA (Autenticación Multifactor)?", ["Sí, en todas", "Sí, en algunas", "Solo en pocas", "No"]),
        ("¿Contraseñas seguras y actualizadas?", ["Sí, con política y gestor", "Sí, pero inconsistentes", "No muy seguras", "No"]),
        ("¿Actualizan el software con parches?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Realizan respaldos diarios?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programado", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacitan al personal regularmente?", ["Sí, al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Hay responsable de backups?", ["Especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ])
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        email = respuestas.pop("correo", "")
        empresa = respuestas.pop("empresa", "")
        sector = respuestas.pop("sector", "")
        pcs = respuestas.pop("pcs", "")
        total_pts = 0
        max_pts = 0
        puntos = {
            "Sí, diario": 3, "Sí, programado": 3, "Sí, al menos 1 vez/año": 3,
            "Automatizado": 3, "Sí, EDR": 3,
            "Sí, formal y probado": 3,
            "Sí, 24/7": 3,
            "Sí, gestionado": 2, "Sí, WPA3 y segmentada": 2,
            "Sí, en todas": 2,
            "Sí, con política y gestor": 2,
            "Especializado": 2
        }
        penalizaciones = {
            "No": -1, "Nunca": -1, "No segura": -1, "No sabe": -1, "No se hace": -1, "No muy seguras": -1
        }
        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                resp = respuestas.get(pregunta)
                if resp in puntos:
                    total_pts += puntos[resp]
                    max_pts += 3
                elif resp in penalizaciones:
                    total_pts += penalizaciones[resp]
                    max_pts += 3
                elif resp:
                    max_pts += 3
        porcentaje = max(0, round((total_pts / max_pts) * 100)) if max_pts else 0

        if email:
            msg = Message("Resultado de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=[email])
            msg.body = f"Empresa: {empresa}
Sector: {sector}
Número de PCs: {pcs}
Postura: {porcentaje}%

Gracias por usar nuestra herramienta."
            mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas, porcentaje=porcentaje, segmentos=segmentos, empresa=empresa, sector=sector, pcs=pcs)
    return render_template('index.html', segmentos=segmentos)
