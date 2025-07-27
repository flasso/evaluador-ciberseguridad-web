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
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Utilizan herramientas de monitoreo del estado de los equipos?",
        "¿Cómo gestionan de manera remota los equipos?",
        "¿Tienen un plan definido de respuesta ante un ataque?",
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿Wi-Fi está segura y separada para invitados?",
    ]),
    ("Protección de Dispositivos", [
        "¿Tienen Antivirus con EDR en todos los equipos?",
        "¿Las contraseñas son seguras y se actualizan periódicamente?",
        "¿Actualizan el sistema operativo y software con parches recientes?",
        "¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?",
    ]),
    ("Respaldo y Conciencia", [
        "¿Respaldan datos críticos a diario?",
        "¿Prueban restauración de respaldos?",
        "¿Capacita regularmente a sus empleados en ciberseguridad?",
        "¿Tiene responsable para las copias de seguridad?",
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, automatizado", "Sí, manual", "Solo al fallar", "No"],
    ["VPN + TeamViewer/AnyDesk", "Solo TeamViewer/AnyDesk", "Acceso no controlado", "No hacen gestión remota"],
    ["Sí, documentado y probado", "Sí, pero no probado", "Sabemos qué hacer, pero no está documentado", "No"],
    ["Sí, gestionado", "Sí, pero mal configurado", "Solo software", "No firewall"],
    ["Personal especializado", "Proveedor MSSP", "Personal no especializado", "No hay firewall"],
    ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"],
    ["Sí, con EDR", "Sí, antivirus básico", "Antivirus gratuito", "No"],
    ["Sí, con política y gestor", "Sí, pero inconsistentes", "Débiles", "No"],
    ["Automatizado", "Manual", "Irregular", "No"],
    ["Sí, en todas", "En algunas", "Pocas", "No"],
    ["Sí, diario", "Semanal", "Mensual", "No"],
    ["Sí, programada", "Ocasional", "Nunca", "No sabe"],
    ["Al menos 1 vez/año", "Sí, informal", "Rara vez", "Nunca"],
    ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]
]

pesos = [2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2]

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
        respuestas_final = []
        idx = 0
        for segmento, preguntas in segmentos:
            for pregunta in preguntas:
                respuesta = respuestas.get(pregunta, "")
                respuestas_final.append((pregunta, respuesta))
                try:
                    posicion = opciones[idx].index(respuesta)
                    if posicion == 0:
                        puntaje += pesos[idx] * 1
                    elif posicion == 1:
                        puntaje += pesos[idx] * 0.66
                    elif posicion == 2:
                        puntaje += pesos[idx] * 0.33
                except:
                    pass
                puntaje_max += pesos[idx]
                idx += 1
        porcentaje = int((puntaje / puntaje_max) * 100)

        # Enviar correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in respuestas_final])

        msg = Message("Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas_final, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)
