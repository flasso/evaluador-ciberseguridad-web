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

# Opciones de número de PCs y sectores
rango_pcs = ["1 a 50", "51 a 150", "151 a 300", "301 a 500", "Más de 500"]
sectores = ["Salud", "Finanzas", "Educación", "Industria", "Tecnología", "Otro"]

# Segmentos y preguntas
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Utilizan herramientas de monitoreo para revisar el estado de salud de los equipos?", ["Sí, diario", "Sí, semanal", "Sí, mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen Antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
        ("¿Tienen un plan definido de respuesta ante incidentes?", ["Sí, documentado y probado", "Sí, documentado", "Solo informal", "No"]),
        ("¿Cómo gestionan de forma remota los equipos?", ["Con herramientas seguras", "Con acceso remoto básico", "Solo presencial", "No lo hacen"]),
    ])
]

# Ponderación personalizada
ponderacion_critica = {
    "¿Respaldan datos críticos a diario?": 2,
    "¿Prueban restauración de respaldos?": 2,
    "¿Capacita regularmente a sus empleados en ciberseguridad?": 2,
    "¿Actualizan el sistema operativo y software con parches recientes?": 2,
    "¿Tienen Antivirus con EDR en todos los equipos?": 2,
    "¿Tienen un plan definido de respuesta ante incidentes?": 2
}

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        empresa = request.form.get('empresa')
        contacto = request.form.get('contacto')
        correo = request.form.get('correo')
        sector = request.form.get('sector')
        pcs = request.form.get('pcs')
        respuestas = {k: v for k, v in request.form.items() if k not in ['empresa', 'contacto', 'correo', 'sector', 'pcs']}

        # Calcular puntaje
        total_obtenido, total_maximo = 0, 0
        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                respuesta = respuestas.get(pregunta)
                if respuesta:
                    idx = opciones.index(respuesta)
                    peso = ponderacion_critica.get(pregunta, 1)
                    if idx == 0:
                        total_obtenido += 3 * peso
                        total_maximo += 3 * peso
                    elif idx == 1:
                        total_obtenido += 2 * peso
                        total_maximo += 3 * peso
                    elif idx == 2:
                        total_obtenido += 1 * peso
                        total_maximo += 3 * peso
                    elif idx == 3:
                        total_maximo += 3 * peso

        porcentaje = round((total_obtenido / total_maximo) * 100) if total_maximo else 0

        # Enviar correo
        msg = Message("Resultado de Evaluación Ciberseguridad",
                      sender="soporte@cloudsoftware.com.co",
                      recipients=["soporte@cloudsoftware.com.co"])
        msg.body = f"""
Empresa: {empresa}
Contacto: {contacto}
Correo: {correo}
Sector: {sector}
Número de PCs: {pcs}
Postura: {porcentaje}%
Respuestas:
""" + "\n".join([f"{k}: {v}" for k, v in respuestas.items()])
        mail.send(msg)

        return render_template('resultados.html', respuestas=respuestas, segmentos=segmentos, porcentaje=porcentaje,
                               empresa=empresa, contacto=contacto, correo=correo, sector=sector, pcs=pcs)
    return render_template('index.html', segmentos=segmentos, sectores=sectores, pcs=rango_pcs)

if __name__ == '__main__':
    app.run(debug=True)
