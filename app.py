from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Lista de preguntas con sus textos y pesos
preguntas_info = [
    ("responsable_ti", "¿Quién es el responsable de TI/ciberseguridad?", 3),
    ("monitoreo_salud", "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?", 3),
    ("inventario", "¿Tienen inventario actualizado de equipos y datos?", 2),
    ("controles", "¿Tienen controles definidos para gestionar la ciberseguridad?", 2),
    ("mfa", "¿Utilizan MFA (Autenticación Multifactor)?", 3),
    ("wifi", "¿Cómo está segmentada y protegida la red Wi-Fi?", 2),
    ("backups", "¿Qué tipo de respaldos realizan?", 5),
    ("restauracion", "¿Han probado la restauración de los respaldos?", 5),
    ("capacitacion", "¿Con qué frecuencia capacitan al personal en ciberseguridad?", 3),
    ("incidentes", "¿Tienen un plan de respuesta ante incidentes?", 4),
    ("induccion", "¿Incluyen seguridad digital en la inducción del personal?", 2),
    ("formacion", "¿Realizan formación continua en seguridad digital?", 2),
    ("gestion_remota", "¿Cómo gestionan los equipos de forma remota?", 4),
    ("parches", "¿Cómo manejan la actualización de software y parches?", 3),
    ("antivirus", "¿Qué tipo de antivirus utilizan?", 5),
    ("seguimiento", "¿Monitorean los eventos de seguridad?", 3),
    ("firewall", "¿Qué tipo de firewall/UTM utilizan?", 4)
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
    ["Propios en oficina", "Arrendados en datacenter", "Mixto", "No tienen"]
]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        form = request.form
        encabezado = {
            "empresa": form.get("empresa"),
            "correo": form.get("correo"),
            "sector": form.get("sector"),
            "pcs": form.get("pcs"),
            "sucursales": form.get("sucursales"),
            "modelo": form.get("modelo"),
            "servidores": form.get("servidores")
        }

        respuestas = []
        puntaje_total = 0
        puntaje_maximo = 0

        for idx, (clave, texto, peso) in enumerate(preguntas_info):
            respuesta = form.get(clave)
            if respuesta:
                try:
                    valor_idx = opciones[idx].index(respuesta)
                except ValueError:
                    valor_idx = 3  # Respuesta inválida = peor calificación
                if valor_idx == 0:
                    puntaje_total += peso
                elif valor_idx == 1:
                    puntaje_total += peso * 0.66
                elif valor_idx == 2:
                    puntaje_total += peso * 0.33
                # valor_idx == 3 no suma nada
            else:
                valor_idx = 3
            puntaje_maximo += peso
            respuestas.append((texto, respuesta))

        porcentaje = int((puntaje_total / puntaje_maximo) * 100) if puntaje_maximo else 0

        # Enviar email
        cuerpo = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{preg}: {resp}" for preg, resp in respuestas])

        msg = Message("Resultado Evaluación Ciberseguridad", sender=app.config['MAIL_USERNAME'], recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", preguntas_info=preguntas_info, opciones=opciones)
