from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Preguntas por segmento
segmentos = [
    ("Gestión y Visibilidad", [
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿La red Wi-Fi es segura y segmentada para invitados?"
    ]),
    ("Protección de Dispositivos", [
        "¿Tienen Antivirus con EDR en todos los equipos?",
        "¿Las contraseñas son seguras y se actualizan periódicamente?",
        "¿Actualizan el sistema operativo y software con parches recientes?",
        "¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Respaldan datos críticos a diario?",
        "¿Prueban la restauración de los respaldos?",
        "¿Capacitan regularmente a sus empleados en ciberseguridad?",
        "¿Tienen un responsable de las copias de seguridad?"
    ]),
    ("Gestión Adicional", [
        "¿Cómo gestionan de forma remota los equipos?",
        "¿Tienen un plan definido de respuesta en caso de un ataque?"
    ])
]

# Opciones para cada pregunta
opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Automatizadas", "Parcialmente", "Manual", "No monitorean"],
    ["Sí, detallado", "Sí, incompleto", "Parcial", "No"],
    ["Sí, con UTM", "Sí, básico", "Solo software", "No tienen"],
    ["Equipo experto", "Proveedor externo", "Personal no especializado", "No tienen firewall"],
    ["Sí, WPA3 y segmentada", "Sí, pero insegura", "Una sola red", "Desconocido"],
    ["Sí, EDR en todos", "Antivirus básico", "Solo algunos equipos", "No tienen"],
    ["Sí, con política y gestor", "Sí, pero débil", "No consistente", "No"],
    ["Automatizado", "Manual", "Irregular", "No actualizan"],
    ["Sí, en todas", "En algunas", "Solo admins", "No tienen MFA"],
    ["Sí, diario", "Semanal", "Mensual", "No hacen backup"],
    ["Sí, programada", "A veces", "Nunca", "No saben"],
    ["Sí, anual o más", "Informal", "Rara vez", "Nunca"],
    ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"],
    ["Con TeamViewer/AnyDesk", "VPN interna", "Visitas físicas", "No gestionan"],
    ["Sí, con roles y pasos claros", "Sí, básico", "No formalizado", "No tienen plan"]
]

# Pesos por importancia
pesos = [1, 2, 1, 2, 2, 1, 3, 1, 3, 2, 4, 4, 3, 2, 2, 3]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        total = 0
        maximo = sum(pesos)
        resultados = []
        for i, (segmento, preguntas) in enumerate(segmentos):
            for pregunta in preguntas:
                r = respuestas.get(pregunta, "No respondida")
                try:
                    idx = opciones[len(resultados)].index(r)
                    if idx == 0:
                        total += pesos[len(resultados)] * 1
                    elif idx == 1:
                        total += pesos[len(resultados)] * 0.66
                    elif idx == 2:
                        total += pesos[len(resultados)] * 0.33
                except:
                    pass
                resultados.append((pregunta, r))

        porcentaje = int((total / maximo) * 100) if maximo else 0

        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in resultados])

        msg = Message("Resultados Evaluación Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=resultados, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)
