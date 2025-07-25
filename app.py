from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'

mail = Mail(app)

# Preguntas organizadas por segmentos
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Utilizan herramientas de monitoreo del estado de los equipos?", ["Sí, monitoreo 24/7", "Sí, semanal", "Solo cuando falla", "No"]),
        ("¿Tienen inventario actualizado de equipos y datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Tienen un plan de respuesta ante incidentes como ransomware?", ["Sí, documentado y probado", "Solo documentado", "Solo una idea general", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, pero mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "Personal no especializado", "No hay firewall"]),
        ("¿El Wi-Fi está seguro y separado para invitados?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR en todos los equipos?", ["Sí, EDR en todos", "Antivirus básico", "Antivirus gratuito", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan los sistemas operativos y software?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Solo en pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos diariamente?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban la restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacitan regularmente a los empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Quién es el responsable de las copias de seguridad?", ["Personal especializado", "Personal no especializado", "Nadie asignado", "No se hace"]),
    ]),
    ("Gestión Remota", [
        ("¿Cómo gestionan los equipos de forma remota?", ["RMM profesional", "TeamViewer/AnyDesk", "Manualmente", "No gestionan"]),
    ])
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        empresa = respuestas.pop("empresa", "")
        correo = respuestas.pop("correo", "")
        telefono = respuestas.pop("telefono", "")
        sector = respuestas.pop("sector", "")
        pcs = respuestas.pop("pcs", "")

        # Calcular puntuación
        puntuacion_total = 0
        max_puntos = 0

        pesos = {
            "¿Respaldan datos críticos diariamente?": 3,
            "¿Prueban la restauración de respaldos?": 3,
            "¿Capacitan regularmente a los empleados en ciberseguridad?": 3,
            "¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?": 3,
            "¿Tienen antivirus con EDR en todos los equipos?": 3,
            "¿Actualizan los sistemas operativos y software?": 3,
        }

        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                respuesta = respuestas.get(pregunta, "")
                try:
                    idx = opciones.index(respuesta)
                    puntaje = 3 - idx
                    peso = pesos.get(pregunta, 1)
                    puntuacion_total += puntaje * peso
                    max_puntos += 3 * peso
                except:
                    continue

        porcentaje = round((puntuacion_total / max_puntos) * 100) if max_puntos > 0 else 0

        # Enviar correo
        try:
            msg = Message("Resultados de Evaluación de Ciberseguridad",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=["soporte@cloudsoftware.com.co"])
            cuerpo = f"""Empresa: {empresa}
Correo: {correo}
Teléfono: {telefono}
Sector: {sector}
Número de PCs: {pcs}
Postura de Ciberseguridad: {porcentaje}%

Respuestas:
"""
            for pregunta, respuesta in respuestas.items():
                cuerpo += f"{pregunta}: {respuesta}\n"
            msg.body = cuerpo
            mail.send(msg)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

        return render_template("resultados.html", respuestas=respuestas, segmentos=segmentos, porcentaje=porcentaje)

    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
