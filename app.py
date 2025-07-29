from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Segmentos y preguntas
segmentos = [
    ("Gestión de TI", [
        "¿Quién es el responsable de TI/ciberseguridad?"
    ]),
    ("Inventario y monitoreo", [
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Controles y políticas", [
        "¿Tienen políticas y controles de ciberseguridad documentados?",
        "¿Utilizan autenticación multifactor (MFA)?",
        "¿Tienen Wi-Fi separado para invitados/clientes?"
    ]),
    ("Respaldos y recuperación", [
        "¿Hacen respaldos periódicos?",
        "¿Han probado la restauración de respaldos?"
    ]),
    ("Cultura de seguridad", [
        "¿Capacitan al personal en ciberseguridad?",
        "¿Tienen un plan de respuesta a incidentes?",
        "¿Hacen simulacros o pruebas de seguridad?",
        "¿Incluyen la ciberseguridad en inducción o entrenamiento inicial?"
    ]),
    ("Infraestructura", [
        "¿Cómo gestionan de manera remota los equipos?",
        "¿Aplican parches y actualizaciones de seguridad?",
        "¿Tienen solución de antivirus o EDR?",
        "¿Utilizan herramientas de monitoreo del entorno?"
    ])
]

# Opciones por pregunta
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
    ["Sí, hacen seguimiento centralizado", "Hay revisión periódica", "Revisión solo ante fallas", "No monitorean"]
]

@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():
    if request.method == "POST":
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        puntaje_total = 0
        puntaje_obtenido = 0
        resultado_preguntas = []

        pesos = {
            6: 5,  # Respaldos
            7: 5,  # Restauración
            9: 4,  # Plan de incidentes
            13: 5, # Parches
            14: 5  # Antivirus
        }

        for idx, (segmento, preguntas) in enumerate(segmentos):
            for pregunta in preguntas:
                respuesta = respuestas.get(pregunta, "No respondido")
                try:
                    idx_opcion = opciones[len(resultado_preguntas)].index(respuesta)
                    peso = pesos.get(len(resultado_preguntas), 3)
                    if idx_opcion == 0:
                        puntaje_obtenido += peso
                    elif idx_opcion == 1:
                        puntaje_obtenido += peso * 0.66
                    elif idx_opcion == 2:
                        puntaje_obtenido += peso * 0.33
                    puntaje_total += peso
                except:
                    pass
                resultado_preguntas.append((pregunta, respuesta))

        porcentaje = round((puntaje_obtenido / puntaje_total) * 100) if puntaje_total else 0

        # Envío de resultados por correo
        cuerpo = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in resultado_preguntas])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=resultado_preguntas, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)
