from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'

mail = Mail(app)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Tienen un plan de respuesta ante incidentes (saben qué hacer si sufren un ataque)?", ["Sí, completo", "Sí, básico", "No definido", "No existe"]),
        ("¿Utilizan herramientas de monitoreo del estado de los equipos?", ["Sí, automáticas y centralizadas", "Parcial", "Revisión manual ocasional", "No"]),
        ("¿Cómo gestionan los equipos de forma remota?", ["Con herramientas seguras", "Conexiones básicas sin seguridad", "Por correo/teléfono", "No gestionan"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Su red Wi-Fi está segmentada y protegida?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen Antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ])
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        empresa = respuestas.get("empresa", "")
        sector = respuestas.get("sector", "")
        equipos = respuestas.get("equipos", "")
        correo = respuestas.get("correo", "")

        # Calcular postura con ponderación
        pesos = {
            "¿Respaldan datos críticos a diario?": 3,
            "¿Prueban restauración de respaldos?": 3,
            "¿Capacita regularmente a sus empleados en ciberseguridad?": 3,
            "¿Actualizan el sistema operativo y software con parches recientes?": 3,
            "¿Tienen Antivirus con EDR en todos los equipos?": 3,
        }
        puntaje_total = 0
        puntaje_obtenido = 0
        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                respuesta = respuestas.get(pregunta, "")
                idx = opciones.index(respuesta) if respuesta in opciones else 0
                ponderado = pesos.get(pregunta, 1)
                max_pts = 3 * ponderado
                puntos = (3 - idx) * ponderado
                puntaje_total += max_pts
                puntaje_obtenido += puntos

        porcentaje = round((puntaje_obtenido / puntaje_total) * 100, 1)

        # Enviar correo
        if correo:
            msg = Message("Resultado Evaluación Ciberseguridad", sender=app.config['MAIL_USERNAME'], recipients=[correo])
            cuerpo = f"""Empresa: {empresa}
Sector: {sector}
Número de PCs: {equipos}
Porcentaje postura: {porcentaje}%
---
Este es el resultado de la evaluación. Recomendamos revisar el informe y contactar un MSP para implementar medidas correctivas.
"""
            msg.body = cuerpo
            mail.send(msg)

        return render_template('resultados.html', respuestas=respuestas, segmentos=segmentos, porcentaje=porcentaje)

    return render_template('index.html', segmentos=segmentos)

# ✅ Render exige esto:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
