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
    ("Gestión de TI", [
        "¿Quién es el responsable de TI/ciberseguridad?"
    ]),
    ("Inventario y monitoreo", [
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Controles y políticas", [
        "¿Tienen políticas de seguridad formalmente definidas?",
        "¿Cómo gestionan las contraseñas?",
        "¿Cómo está configurada su red Wi-Fi?"
    ]),
    ("Respaldos y recuperación", [
        "¿Qué frecuencia tienen sus respaldos?",
        "¿Realizan pruebas de recuperación?"
    ]),
    ("Cultura de seguridad", [
        "¿Con qué frecuencia capacitan al personal en ciberseguridad?",
        "¿Tienen un protocolo claro ante incidentes?",
        "¿Capacitan al nuevo personal en seguridad?",
        "¿Realizan simulacros de ciberseguridad?"
    ]),
    ("Infraestructura", [
        "¿Cómo gestionan los equipos de forma remota?",
        "¿Qué tan actualizados están los sistemas operativos y software?",
        "¿Qué tipo de antivirus usan?",
        "¿Cómo monitorean la infraestructura tecnológica?",
        "¿Tienen firewall o UTM si tienen servidores en la oficina?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, con alertas y reportes automáticos", "Sí, manualmente", "Solo cuando hay problemas", "No"],
    ["Sí, actualizado mensualmente", "Sí, pero con retrasos", "Parcial", "No"],
    ["Sí, con controles definidos", "Solo antivirus", "Lo maneja proveedor", "No tienen"],
    ["Sí, con doble autenticación (MFA)", "Contraseñas fuertes", "Contraseñas básicas", "Sin política"],
    ["Sí, red separada y cifrada", "Solo clave segura", "Compartida con clientes", "Abierta"],
    ["Sí, con backup diario probado", "Backup semanal", "Backup sin prueba", "No hacen respaldo"],
    ["Sí, se hacen pruebas de recuperación", "Solo respaldan", "No han probado nunca", "No saben"],
    ["Sí, cada mes", "Cada semestre", "Una vez al año", "Nunca"],
    ["Sí, tienen protocolo y responsable", "Hay una guía básica", "Solo reacción espontánea", "No saben qué hacer"],
    ["Sí, al menos cada 6 meses", "Una vez al año", "Solo nuevo personal", "Nunca"],
    ["Sí, reciben formación y simulacros", "Capacitación básica", "Solo charlas internas", "Nunca"],
    ["Sí, con monitoreo remoto y soporte", "Solo soporte en sitio", "Uso Team/AnyDesk sin control", "Ninguno"],
    ["Sí, con parches automáticos", "Solo críticas", "Depende del proveedor", "No actualizan"],
    ["Antivirus con EDR", "Antivirus tradicional", "Solo Windows Defender", "No tiene"],
    ["Sí, hacen seguimiento centralizado", "Hay revisión periódica", "Revisión solo ante fallas", "No monitorean"],
    ["Sí", "No", "Lo desconozco", "No aplica"]
]

@app.route('/')
def index():
    return render_template("index.html", segmentos=segmentos, opciones=opciones)

@app.route('/evaluacion', methods=['POST'])
def evaluacion():
    respuestas = dict(request.form)
    encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}

    resultado_respuestas = []
    puntaje = 0
    total = 0

    i = 0
    for _, preguntas in segmentos:
        for pregunta in preguntas:
            respuesta = respuestas.get(pregunta, '')
            if respuesta in opciones[i]:
                valor = opciones[i].index(respuesta)
                score = 3 - valor
            else:
                score = 0
            resultado_respuestas.append((pregunta, respuesta))
            puntaje += score
            total += 3
            i += 1

    porcentaje = int((puntaje / total) * 100)

    msg = Message("Resultados de Evaluación de Ciberseguridad",
                  sender="soporte@cloudsoftware.com.co",
                  recipients=["soporte@cloudsoftware.com.co"])
    cuerpo = f"Empresa: {encabezado['empresa']}\nCorreo: {encabezado['correo']}\nSector: {encabezado['sector']}\nN° de PCs: {encabezado['pcs']}\nSucursales: {encabezado['sucursales']}\nModelo de Trabajo: {encabezado['modelo']}\nServidores: {encabezado['servidores']}\nPostura: {porcentaje}%\n\nRespuestas:\n"
    cuerpo += "\n".join([f"{p}: {r}" for p, r in resultado_respuestas])
    msg.body = cuerpo
    mail.send(msg)

    return render_template("resultados.html", porcentaje=porcentaje, respuestas=resultado_respuestas, encabezado=encabezado)