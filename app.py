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
    ("Gestión y Planeación", [
        ("¿Quién es el responsable de TI/ciberseguridad?", 2),
        ("¿Utilizan herramientas de monitoreo del estado de los equipos?", 2),
        ("¿Cómo gestionan de forma remota los equipos?", 2),
        ("¿Tienen un plan definido de respuesta ante incidentes?", 3),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", 3),
        ("¿Quién gestiona el firewall?", 2),
        ("¿Wi-Fi está segura y separada para invitados?", 2),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen Antivirus con EDR en todos los equipos?", 3),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", 2),
        ("¿Actualizan el sistema operativo y software con parches recientes?", 3),
        ("¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?", 2),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", 3),
        ("¿Prueban restauración de respaldos?", 3),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", 3),
        ("¿Tiene responsable para las copias de seguridad?", 2),
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, 24/7 automatizado", "Sí, ocasional", "Solo si falla algo", "No se monitorea"],
    ["Herramientas tipo TeamViewer/AnyDesk", "VPN y control remoto", "Solo presencial", "No gestionamos"],
    ["Sí, documentado y conocido", "Sí, pero informal", "No saben qué hacer", "No tienen plan"],
    ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No tienen"],
    ["Experto interno", "Proveedor externo", "Personal no especializado", "No aplica"],
    ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"],
    ["Sí, con EDR", "Sí, antivirus básico", "Solo antivirus gratuito", "No"],
    ["Sí, con política y gestor", "Sí, pero no formal", "No actualizan", "No tienen"],
    ["Automatizado", "Manual regular", "Irregular", "No actualizan"],
    ["Sí, en todas", "Sí, en algunas", "Muy pocas", "No tienen"],
    ["Sí, diario", "Semanal", "Mensual", "No hacen backup"],
    ["Sí, programada", "Ocasional", "Nunca", "No sabe"],
    ["Sí, mínimo 1 vez/año", "Sí, informal", "Rara vez", "Nunca"],
    ["Especialista asignado", "TI no especializado", "Nadie asignado", "No se hace"]
]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        puntaje = 0
        puntaje_max = 0
        puntajes_individuales = []
        for i, (segmento, preguntas) in enumerate(segmentos):
            for j, (pregunta, peso) in enumerate(preguntas):
                idx = sum(len(p) for _, p in segmentos[:i]) + j
                respuesta = respuestas.get(pregunta, "")
                try:
                    valor = opciones[idx].index(respuesta)
                    if valor == 0:
                        puntaje += peso * 1
                    elif valor == 1:
                        puntaje += peso * 0.66
                    elif valor == 2:
                        puntaje += peso * 0.33
                except:
                    valor = -1
                puntaje_max += peso
                puntajes_individuales.append((pregunta, respuesta))
        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        # Enviar correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{pregunta}: {respuesta}" for pregunta, respuesta in puntajes_individuales])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=puntajes_individuales, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
