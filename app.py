from flask import Flask, render_template, request, redirect, url_for
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
        "¿Utilizan herramientas de monitoreo para los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿La red Wi-Fi está protegida y segmentada?"
    ]),
    ("Protección de Dispositivos", [
        "¿Utilizan Antivirus con EDR en todos los equipos?",
        "¿Las contraseñas son seguras y se actualizan periódicamente?",
        "¿Actualizan los sistemas con los últimos parches?",
        "¿Tienen activada la MFA (Autenticación Multifactor)?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Respaldan información crítica a diario?",
        "¿Realizan pruebas de restauración periódicas?",
        "¿Capacitan regularmente a su personal en ciberseguridad?",
        "¿Hay un responsable para gestionar los respaldos?"
    ]),
    ("Planeación y Contingencia", [
        "¿Cómo gestionan de forma remota los dispositivos?",
        "¿Tienen un plan definido en caso de un ataque como ransomware?",
        "¿Qué tipo de servidores utilizan?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, monitoreo diario", "Sí, monitoreo ocasional", "Solo si falla", "No"],
    ["Sí, detallado", "Sí, pero incompleto", "Parcial", "No"],
    ["Sí, bien configurado", "Sí, pero mal configurado", "Solo software", "No"],
    ["Experto interno", "Proveedor externo", "Personal no especializado", "No hay gestión"],
    ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"],
    ["Sí, EDR", "Antivirus comercial", "Gratuito", "No"],
    ["Política definida y gestor", "Sí, pero débil", "No realmente", "No"],
    ["Automatizadas", "Manuales", "Ocasionales", "No actualizan"],
    ["Sí, en todas las cuentas", "Sí, en algunas", "Solo correo", "No"],
    ["Sí, respaldos diarios", "Semanal", "Mensual", "No respaldan"],
    ["Sí, pruebas programadas", "Solo al instalar", "Nunca", "No saben"],
    ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"],
    ["Especialista dedicado", "TI no especializado", "Nadie asignado", "No se hace"],
    ["VPN + herramientas (TeamViewer, AnyDesk)", "VPN sin control", "Software inseguro", "No gestionan"],
    ["Sí, con roles claros", "Solo TI sabe qué hacer", "Solo respaldos", "No hay plan"],
    ["Propios", "Arrendados", "Ambos", "No tiene"]
]

pesos = [2, 2, 2, 3, 3, 2, 4, 3, 4, 3, 5, 5, 4, 3, 2, 3, 2]

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
        detalles = []
        for idx, (segmento, preguntas) in enumerate(segmentos):
            for p in preguntas:
                respuesta = respuestas.get(p, "")
                try:
                    valor = opciones[idx * 4 + preguntas.index(p)].index(respuesta)
                    if valor == 0:
                        puntaje += pesos[idx * 4 + preguntas.index(p)]
                    elif valor == 1:
                        puntaje += pesos[idx * 4 + preguntas.index(p)] * 0.66
                    elif valor == 2:
                        puntaje += pesos[idx * 4 + preguntas.index(p)] * 0.33
                    # 3 y 4 no suman
                except:
                    pass
                puntaje_max += pesos[idx * 4 + preguntas.index(p)]
                detalles.append((p, respuesta))

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
""" + "\n".join([f"{pregunta}: {respuesta}" for pregunta, respuesta in detalles])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=detalles, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)
