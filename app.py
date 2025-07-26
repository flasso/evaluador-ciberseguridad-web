from flask import Flask, render_template, request, redirect, url_for
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

# Segmentos de preguntas
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", 1),
        ("¿Utilizan herramientas de monitoreo del estado de los equipos?", 1),
        ("¿Tienen inventario actualizado de equipos/datos?", 1),
        ("¿Cómo gestionan los equipos de forma remota?", 1),
        ("¿Tienen un plan de respuesta a incidentes definido?", 2),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", 2),
        ("¿Quién gestiona el firewall?", 2),
        ("¿La red Wi-Fi está segura y separada para invitados?", 1),
    ]),
    ("Protección de Dispositivos", [
        ("¿Utilizan antivirus con EDR en todos los equipos?", 3),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", 1),
        ("¿Actualizan el sistema operativo y software con parches recientes?", 2),
        ("¿MFA (Autenticación Multifactor) está activada en cuentas críticas?", 2),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", 3),
        ("¿Prueban la restauración de respaldos regularmente?", 3),
        ("¿Capacitan regularmente a sus empleados en ciberseguridad?", 3),
        ("¿Quién es el responsable de las copias de seguridad?", 1),
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, diario/24x7", "Semanal", "Mensual", "No"],
    ["Sí, detallado", "Sí, incompleto", "Parcial", "No"],
    ["TeamViewer/AnyDesk con acceso seguro", "VPN corporativa", "Herramientas abiertas", "No gestionan"],
    ["Sí, documentado", "Informal o verbal", "Parcial", "No saben qué hacer"],
    ["Sí, gestionado y actualizado", "Sí, pero mal configurado", "Solo software básico", "No tienen"],
    ["Personal especializado", "Proveedor MSSP", "Personal no especializado", "No hay responsable"],
    ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No tienen"],
    ["Sí, EDR en todos", "Antivirus comercial", "Gratis", "No tienen"],
    ["Sí, política y gestor", "Sí, pero inconsistente", "Sin control real", "No tienen"],
    ["Automático", "Manual regular", "Esporádico", "No actualizan"],
    ["Sí, en todos los accesos", "En algunos", "Solo administrativos", "No tienen"],
    ["Sí, diario", "Semanal", "Mensual", "No hacen"],
    ["Sí, pruebas programadas", "Solo al instalar", "Nunca", "No saben cómo"],
    ["Al menos 1 vez al año", "Ocasional o informal", "Muy pocas veces", "Nunca"],
    ["TI especializado", "TI no especializado", "Nadie asignado", "No hacen backup"],
]

pesos = [x[1] for segmento in segmentos for x in segmento]
preguntas = [x[0] for segmento in segmentos for x in segmento]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        empresa = respuestas.pop("empresa", "No especificado")
        correo = respuestas.pop("correo", "No especificado")
        sector = respuestas.pop("sector", "No especificado")
        pcs = respuestas.pop("pcs", "No especificado")
        sucursales = respuestas.pop("sucursales", "No especificado")
        modalidad = respuestas.pop("modalidad", "No especificado")
        servidores = respuestas.pop("servidores", "No especificado")

        puntuacion = 0
        maximo = 0
        detalle = []

        for idx, pregunta in enumerate(preguntas):
            respuesta = respuestas.get(pregunta, "")
            try:
                opcion_idx = opciones[idx].index(respuesta)
                puntos = 3 - opcion_idx
                if puntos < 0:
                    puntos = 0
                puntuacion += puntos * pesos[idx]
                maximo += 3 * pesos[idx]
                detalle.append((pregunta, respuesta, puntos * pesos[idx]))
            except:
                detalle.append((pregunta, "No respondido", 0))

        porcentaje = round((puntuacion / maximo) * 100) if maximo > 0 else 0

        if correo and correo != "No especificado":
            msg = Message("Resultado de Evaluación de Ciberseguridad",
                          sender='soporte@cloudsoftware.com.co',
                          recipients=[correo])
            msg.body = f"""Empresa: {empresa}
Sector: {sector}
Número de PCs: {pcs}
Sucursales: {sucursales}
Modalidad: {modalidad}
Servidores: {servidores}
Postura de Ciberseguridad: {porcentaje}%
            """
            try:
                mail.send(msg)
            except Exception as e:
                print("No se pudo enviar el correo:", e)

        return render_template("resultados.html", empresa=empresa, porcentaje=porcentaje,
                               detalle=detalle, sector=sector, pcs=pcs,
                               sucursales=sucursales, modalidad=modalidad, servidores=servidores)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
