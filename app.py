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
        ("¿Quién es el responsable de TI/ciberseguridad?", [
            "Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"
        ]),
        ("¿Utilizan herramientas de monitoreo del estado de salud de los equipos?", [
            "Sí, automatizadas", "Sí, parciales", "Manual y esporádico", "No monitorean"
        ]),
        ("¿Tienen inventario actualizado de equipos/datos?", [
            "Sí, detallado", "Sí, incompleto", "Parcial", "No"
        ]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", [
            "Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"
        ]),
        ("¿Quién gestiona el firewall?", [
            "Experto interno", "Proveedor MSSP", "Personal no especializado", "No hay firewall"
        ]),
        ("¿Wi-Fi está segura y separada para invitados?", [
            "Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"
        ]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Cuentan con Antivirus con EDR en todos los equipos?", [
            "Sí, EDR en todos", "Antivirus básico", "Antivirus gratuito", "No"
        ]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", [
            "Política definida + gestor", "Sí, pero inconsistente", "No realmente", "No"
        ]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", [
            "Automatizado", "Manual", "Irregular", "No"
        ]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", [
            "Sí, en todas", "Sí, en algunas", "En pocas", "No"
        ]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", [
            "Sí, diario", "Semanal", "Mensual", "No"
        ]),
        ("¿Prueban restauración de respaldos?", [
            "Sí, programada", "Ocasional", "Nunca", "No sabe"
        ]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", [
            "Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"
        ]),
        ("¿Tiene responsable para las copias de seguridad?", [
            "Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"
        ]),
        ("¿Cómo gestionan de manera remota los equipos?", [
            "Con herramientas tipo RMM", "TeamViewer/AnyDesk", "Acceso remoto básico", "No se gestiona"
        ]),
        ("¿Tienen un plan definido de respuesta ante incidentes?", [
            "Sí, con pruebas periódicas", "Sí, pero sin pruebas", "Plan informal", "No"
        ]),
    ])
]

pesos = {
    "¿Respaldan datos críticos a diario?": 3,
    "¿Prueban restauración de respaldos?": 3,
    "¿Capacita regularmente a sus empleados en ciberseguridad?": 3,
    "¿Actualizan el sistema operativo y software con parches recientes?": 3,
    "¿Cuentan con Antivirus con EDR en todos los equipos?": 3,
    "¿Tienen un plan definido de respuesta ante incidentes?": 3
}

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        empresa = respuestas.pop("empresa", "")
        contacto = respuestas.pop("contacto", "")
        sector = respuestas.pop("sector", "")
        pcs = respuestas.pop("pcs", "")
        servidores = respuestas.pop("servidores", "")
        sedes = respuestas.pop("sedes", "")
        modelo = respuestas.pop("modelo", "")

        total_obtenido = 0
        total_posible = 0

        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                respuesta = respuestas.get(pregunta, "")
                peso = pesos.get(pregunta, 1)
                if respuesta in opciones:
                    idx = opciones.index(respuesta)
                    if idx == 0:
                        total_obtenido += 3 * peso
                    elif idx == 1:
                        total_obtenido += 2 * peso
                    elif idx == 2:
                        total_obtenido += 1 * peso
                total_posible += 3 * peso

        porcentaje = round((total_obtenido / total_posible) * 100, 1)

        # Enviar correo
        cuerpo = f"""Empresa: {empresa}
Contacto: {contacto}
Sector: {sector}
Número de PCs: {pcs}
Servidores: {servidores}
Sedes: {sedes}
Modelo: {modelo}
Postura: {porcentaje}%

Respuestas:
"""
        for pregunta, respuesta in respuestas.items():
            cuerpo += f"{pregunta}: {respuesta}\n"

        msg = Message("Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas, segmentos=segmentos,
                               empresa=empresa, contacto=contacto, sector=sector, pcs=pcs,
                               porcentaje=porcentaje, servidores=servidores, sedes=sedes, modelo=modelo)
    return render_template('index.html', segmentos=segmentos)
