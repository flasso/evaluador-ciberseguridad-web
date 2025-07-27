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
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿El Wi-Fi es seguro y segmentado para invitados?"
    ]),
    ("Protección de Dispositivos", [
        "¿Cuentan con antivirus con EDR en todos los dispositivos?",
        "¿Usan contraseñas seguras y políticas de actualización?",
        "¿Actualizan el software y sistema operativo con regularidad?",
        "¿Tienen MFA (Autenticación Multifactor) activado en cuentas críticas?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Realizan respaldos diarios de la información crítica?",
        "¿Han probado la restauración de sus respaldos?",
        "¿Capacitan a los empleados en ciberseguridad regularmente?",
        "¿Tienen responsable para la gestión de backups?"
    ]),
    ("Planeación y Continuidad", [
        "¿Cómo gestionan los equipos de forma remota?",
        "¿Tienen un plan definido en caso de un ataque de ransomware?",
        "¿Monitorean los servidores internos de forma activa?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Automatizado diariamente", "Semanal", "Mensual", "No lo hacen"],
    ["Sí, detallado", "Sí, incompleto", "Parcial", "No"],
    ["Sí, y está gestionado correctamente", "Sí, pero mal configurado", "Solo software", "No tiene"],
    ["Equipo interno especializado", "Proveedor externo (MSSP)", "Personal no especializado", "No se gestiona"],
    ["Sí, WPA3 y segmentado", "Sí, pero débil", "No seguro", "No lo tienen"],
    ["Sí, EDR en todos", "Sí, antivirus básico", "Antivirus gratuito", "No tienen"],
    ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No tienen política"],
    ["Automatizado", "Manual", "Irregular", "Nunca actualizan"],
    ["Sí, en todas las cuentas", "Sí, en algunas", "Solo en pocas", "No usan MFA"],
    ["Sí, diario", "Semanal", "Mensual", "No hacen respaldos"],
    ["Sí, de forma programada", "Ocasionalmente", "Nunca", "No lo saben"],
    ["Al menos 1 vez al año", "Sí, pero informal", "Rara vez", "Nunca"],
    ["Personal especializado", "Personal no especializado", "Nadie asignado", "No se hace"],
    ["Con software como TeamViewer o AnyDesk", "Manual por llamada o videollamada", "No hacen gestión remota", "No aplica"],
    ["Sí, documentado y probado", "Sí, pero no probado", "Informal", "No tienen plan"],
    ["Sí, con alertas activas", "Sí, pero sin alertas", "Manual y ocasional", "No hacen monitoreo"]
]

pesos = [
    2, 2, 2,  # Gestión
    3, 3, 2,  # Red
    4, 2, 3, 3,  # Dispositivos
    4, 3, 3, 2,  # Respaldos
    2, 3, 2  # Planeación
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

        for i, pregunta in enumerate(sum([s[1] for s in segmentos], [])):
            respuesta = respuestas.get(pregunta, "")
            valor = opciones[i].index(respuesta) if respuesta in opciones[i] else 3
            peso = pesos[i]
            if valor == 0:
                puntaje += peso
            elif valor == 1:
                puntaje += peso * 0.66
            elif valor == 2:
                puntaje += peso * 0.33
            # valor == 3 no suma
            puntaje_max += peso
            puntajes_individuales.append((pregunta, respuesta))

        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        # Enviar por correo
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

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender=app.config['MAIL_USERNAME'], recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=puntajes_individuales, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)
