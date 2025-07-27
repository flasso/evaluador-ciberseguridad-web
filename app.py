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
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Tienen inventario actualizado de equipos y datos?",
        "¿Utilizan herramientas de monitoreo?",
        "¿Cómo gestionan remotamente los equipos?",
        "¿Tienen un plan de respuesta ante incidentes?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿Su Wi-Fi está segura y segmentada?"
    ]),
    ("Protección de Dispositivos", [
        "¿Cuentan con Antivirus con EDR?",
        "¿Las contraseñas son seguras y se actualizan periódicamente?",
        "¿Se actualiza el software con los últimos parches?",
        "¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Se realizan respaldos diarios?",
        "¿Se prueban las restauraciones de respaldo?",
        "¿Se capacita regularmente al personal en ciberseguridad?",
        "¿Hay un responsable para los respaldos?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Personal interno", "Proveedor externo", "Ninguno"],
    ["Sí, completo", "Sí, parcial", "Solo equipos", "No hay inventario"],
    ["Sí, 24/7", "Sí, parcial", "Solo alertas", "No usan"],
    ["TeamViewer/AnyDesk", "VPN y conexión remota", "Visita física", "No se gestiona"],
    ["Sí, probado", "Sí, no probado", "Algo definido", "No saben qué hacer"],
    ["Sí, configurado", "Sí, no gestionado", "Solo software", "No tiene"],
    ["Especialista interno", "Proveedor externo", "Personal no especializado", "No se gestiona"],
    ["WPA3 y segmentada", "WPA2, no segmentada", "Abierta", "No tiene Wi-Fi"],
    ["Sí, EDR en todos", "Sí, antivirus básico", "Solo algunos", "No hay protección"],
    ["Sí, política y gestor", "Sí, parcialmente", "No tienen política", "No hay control"],
    ["Automatizado", "Manual", "Ocasional", "No actualizan"],
    ["Sí, en todos los accesos", "Sí, solo críticos", "Solo en algunos", "No tienen MFA"],
    ["Sí, diarios", "Sí, semanales", "Mensuales", "No se hacen"],
    ["Sí, regularmente", "A veces", "Nunca", "No saben"],
    ["Sí, anual o más", "Capacitación informal", "Ocasional", "Nunca"],
    ["Especialista", "TI no especializado", "Empleado cualquiera", "No hay responsable"]
]

pesos = [3, 2, 3, 2, 3, 3, 3, 2, 4, 3, 4, 3, 4, 4, 3, 3]

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
        detalle = []

        for idx, (pregunta) in enumerate(sum([q[1] for q in segmentos], [])):
            respuesta = respuestas.get(pregunta, "")
            try:
                nivel = opciones[idx].index(respuesta)
                if nivel == 0:
                    puntaje += pesos[idx] * 1.0
                elif nivel == 1:
                    puntaje += pesos[idx] * 0.66
                elif nivel == 2:
                    puntaje += pesos[idx] * 0.33
            except:
                nivel = -1
            puntaje_max += pesos[idx]
            detalle.append((pregunta, respuesta))

        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in detalle])

        msg = Message("Resultado de Evaluación de Ciberseguridad", sender=app.config['MAIL_USERNAME'], recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=detalle, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
