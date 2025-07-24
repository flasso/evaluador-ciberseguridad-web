from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de correo con Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'

mail = Mail(app)

# Preguntas y opciones agrupadas por categoría
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Sí, diariamente", "Sí, semanalmente", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Tienen un plan de respuesta ante incidentes?", ["Sí, documentado y probado", "Sí, documentado pero no probado", "No formal", "No"]),
        ("¿Monitorean el estado de salud de los equipos?", ["Sí, diario", "Sí, semanal", "Solo cuando fallan", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall o UTM en la red?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿El Wi-Fi está segmentado y protegido?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Se aplican actualizaciones y parches?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Cuentan con MFA (Autenticación Multifactor) en cuentas clave?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
        ("¿Cómo gestionan los equipos a distancia?", ["Herramientas seguras (ej. RMM)", "TeamViewer/AnyDesk con control", "Compartir credenciales", "No tienen gestión remota"]),
    ]),
    ("Respaldos y Concienciación", [
        ("¿Respaldan datos críticos?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban los respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacitan en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Quién gestiona los respaldos?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ]),
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = request.form.to_dict()
        encabezado = {
            "empresa": respuestas.pop("empresa", ""),
            "contacto": respuestas.pop("contacto", ""),
            "email": respuestas.pop("email", ""),
            "sector": respuestas.pop("sector", ""),
            "pcs": respuestas.pop("pcs", "")
        }

        puntaje = 0
        max_puntaje = len(respuestas) * 3
        pesos_3 = ["Dedicado y certificado", "Sí, diariamente", "Sí, detallado", "Sí, documentado y probado", "Sí, diario",
                   "Sí, gestionado", "Sí, WPA3 y segmentada", "Sí, EDR", "Sí, con política definida y gestor",
                   "Automatizado", "Sí, en todas", "Herramientas seguras (ej. RMM)", "Sí, programada",
                   "Al menos 1 vez/año", "Personal especializado"]
        pesos_2 = ["Interno no exclusivo", "Sí, semanalmente", "Sí, incompleto", "Sí, documentado pero no probado", "Sí, semanal",
                   "Sí, mal configurado", "Sí, pero débil", "Sí, antivirus básico", "Sí, pero inconsistente", "Manual",
                   "Sí, en algunas", "TeamViewer/AnyDesk con control", "Ocasional", "Sí, pero informal", "TI no especializado"]

        for r in respuestas.values():
            if r in pesos_3:
                puntaje += 3
            elif r in pesos_2:
                puntaje += 2
            else:
                puntaje += 1

        porcentaje = round(puntaje / max_puntaje * 100)

        html_resultado = render_template(
            'resultados.html',
            respuestas=respuestas,
            segmentos=segmentos,
            encabezado=encabezado,
            porcentaje=porcentaje
        )

        # Enviar por correo
        msg = Message(subject=f"Resultados Evaluación de Seguridad - {encabezado['empresa']}",
                      recipients=[encabezado["email"]],
                      sender=app.config['MAIL_USERNAME'],
                      html=html_resultado)
        mail.send(msg)

        return html_resultado

    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
