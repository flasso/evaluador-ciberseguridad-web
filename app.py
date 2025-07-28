from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Segmentos de preguntas y sus pesos
segmentos = [
    ("Gestión de TI", [
        ("¿Quién es el responsable de TI/ciberseguridad?", 3)
    ]),
    ("Inventario y monitoreo", [
        ("¿Utilizan herramientas de monitoreo del estado de salud de los equipos?", 2),
        ("¿Tienen inventario actualizado de equipos y datos?", 2)
    ]),
    ("Controles y políticas", [
        ("¿Tienen políticas formales de ciberseguridad?", 2),
        ("¿Usan autenticación multifactor (MFA)?", 3),
        ("¿La red Wi-Fi de su empresa está protegida?", 2)
    ]),
    ("Respaldos y recuperación", [
        ("¿Con qué frecuencia respaldan su información?", 4),
        ("¿Han probado la restauración de los respaldos?", 4)
    ]),
    ("Cultura de seguridad", [
        ("¿Realizan simulacros o pruebas de seguridad?", 2),
        ("¿Tienen un plan de respuesta ante incidentes?", 4),
        ("¿Capacitan regularmente al personal?", 3),
        ("¿Hacen campañas de concientización?", 2)
    ]),
    ("Infraestructura", [
        ("¿Cómo gestionan los equipos de forma remota?", 3),
        ("¿Actualizan regularmente los sistemas?", 4),
        ("¿Qué tipo de antivirus usan?", 4),
        ("¿Monitorean la seguridad de sus dispositivos?", 2),
        ("¿Dónde están sus servidores?", 2)
    ])
]

# Opciones por pregunta (en el mismo orden que las preguntas)
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
    ["Propios en oficina", "Arrendados en datacenter", "Mixto", "No tienen"]
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
        idx = 0
        for segmento, preguntas in segmentos:
            for pregunta, peso in preguntas:
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
                idx += 1

        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        # Enviar por correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{pregunta}: {respuesta}" for pregunta, respuesta in puntajes_individuales])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=puntajes_individuales, porcentaje=porcentaje, encabezado=encabezado)
    
    return render_template("index.html", segmentos=segmentos, opciones=opciones)

# BLOQUE NECESARIO PARA RENDER.COM
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
