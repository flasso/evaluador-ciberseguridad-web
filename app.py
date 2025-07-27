from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

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
        "¿Tienen inventario actualizado de equipos y datos?",
        "¿Tienen un plan definido de respuesta en caso de ataque?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿La red Wi-Fi está segura y segmentada para invitados?"
    ]),
    ("Protección de Dispositivos", [
        "¿Utilizan Antivirus con EDR?",
        "¿Las contraseñas son seguras y se actualizan periódicamente?",
        "¿Actualizan el sistema operativo y software con parches recientes?",
        "¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?",
        "¿Cómo gestionan de forma remota los equipos?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Realizan respaldos diarios de los datos críticos?",
        "¿Prueban la restauración de respaldos regularmente?",
        "¿Capacita regularmente a sus empleados en ciberseguridad?",
        "¿Quién es el responsable de las copias de seguridad?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, con herramientas proactivas", "Sí, pero limitado", "Solo manual", "No se revisa"],
    ["Sí, detallado", "Sí, incompleto", "Parcial", "No"],
    ["Sí, documentado y probado", "Sí, pero no probado", "Solo ideas generales", "No existe"],
    ["Sí, gestionado", "Sí, mal configurado", "Solo firewall software", "No firewall"],
    ["Experto interno", "Proveedor MSP", "Personal no especializado", "No se gestiona"],
    ["Sí, WPA3 y segmentada", "Sí, pero sin separación", "No segura", "No"],
    ["Sí, EDR", "Sí, antivirus básico", "Antivirus gratuito", "No"],
    ["Sí, con política y gestor", "Sí, pero inconsistente", "No realmente", "No"],
    ["Automatizado", "Manual", "Irregular", "No"],
    ["Sí, en todas", "Sí, en algunas", "Solo en pocas", "No"],
    ["Con soluciones como TeamViewer, AnyDesk", "Manual presencial", "Combinado", "No se realiza"],
    ["Sí, diario", "Semanal", "Mensual", "No"],
    ["Sí, programada", "Ocasional", "Nunca", "No sabe"],
    ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"],
    ["Personal especializado", "Personal no especializado", "Nadie asignado", "No se hace"]
]

pesos = [
    2, 2, 2, 3, 3, 3, 2,
    4, 3, 4, 4, 2,
    4, 4, 4, 3
]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        
        puntaje_total = 0
        puntaje_maximo = 0
        respuestas_mostradas = []
        
        for i, (segmento, preguntas) in enumerate(segmentos):
            for pregunta in preguntas:
                respuesta = respuestas.get(pregunta)
                opciones_pregunta = opciones.pop(0)
                peso = pesos.pop(0)
                try:
                    indice = opciones_pregunta.index(respuesta)
                    if indice == 0:
                        puntaje_total += peso
                    elif indice == 1:
                        puntaje_total += peso * 0.66
                    elif indice == 2:
                        puntaje_total += peso * 0.33
                except:
                    pass
                puntaje_maximo += peso
                respuestas_mostradas.append((pregunta, respuesta))

        porcentaje = int((puntaje_total / puntaje_maximo) * 100) if puntaje_maximo > 0 else 0

        # Enviar correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in respuestas_mostradas])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", porcentaje=porcentaje, respuestas=respuestas_mostradas, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
