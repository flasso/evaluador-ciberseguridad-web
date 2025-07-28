from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

segmentos = [
    ("Gestión y Planeación", [
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Tienen inventario actualizado de equipos y datos?",
        "¿Tienen un plan definido de respuesta en caso de un ataque?",
        "¿Capacitan regularmente a su personal sobre ciberseguridad?",
    ]),
    ("Estado y Protección de Equipos", [
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Cómo gestionan de forma remota los dispositivos?",
        "¿El software de los equipos se mantiene actualizado con parches de seguridad?",
        "¿Tienen instalado un antivirus con EDR activo y funcional?",
    ]),
    ("Respaldos y recuperación", [
        "¿Realizan copias de seguridad (backups)?",
        "¿Con qué frecuencia verifican y prueban sus backups?",
        "¿Las copias de seguridad están almacenadas de forma segura (local y/o en la nube)?",
        "¿Cuentan con capacidad para restaurar información ante un incidente?",
    ]),
    ("Accesos y Redes", [
        "¿Utilizan autenticación multifactor (MFA) en sus sistemas críticos?",
        "¿Su red Wi-Fi está segmentada para invitados y uso interno?",
        "¿Sus contraseñas cumplen con buenas prácticas (complejidad, renovación)?",
        "¿Tienen firewall o UTM gestionado correctamente?",
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, actualizado y verificado", "Sí, pero no actualizado", "Parcial", "No se tiene"],
    ["Sí, probado y documentado", "Existe pero no probado", "En desarrollo", "No tienen plan"],
    ["Sí, al menos anual", "Ocasional", "Rara vez", "Nunca"],
    ["Sí, con alertas automatizadas", "Manual ocasional", "Solo al fallar", "No monitorean"],
    ["Acceso remoto seguro (VPN/RDP/Mobile Device Mgmt)", "Con herramientas como TeamViewer/AnyDesk", "Acceso remoto libre", "No tienen forma de acceso remoto"],
    ["Sí, todos actualizados", "Algunos equipos actualizados", "Solo sistema operativo", "No actualizan regularmente"],
    ["Sí, con licencias activas", "Sí, pero sin EDR", "Gratuito o desactualizado", "No usan antivirus"],
    ["Sí, diarios", "Semanalmente", "Mensualmente", "No hacen backups"],
    ["Sí, con pruebas frecuentes", "Se prueban de vez en cuando", "No se prueban", "No se sabe"],
    ["Sí, en nube y local", "Solo en la nube", "Solo local", "No se sabe dónde están"],
    ["Sí, probado recientemente", "Sí, pero no probado", "Proceso complejo/no documentado", "No podrían recuperar datos"],
    ["Sí, en todos los sistemas críticos", "Solo en algunos", "Lo están implementando", "No usan MFA"],
    ["Sí, redes separadas", "Una sola red con contraseña", "Red abierta", "No tienen Wi-Fi"],
    ["Sí, complejas y se actualizan", "Solo complejas", "Misma contraseña en todos", "Sin control de contraseñas"],
    ["Sí, UTM o firewall administrado", "Solo firewall básico", "Sin configuración", "No tienen firewall"],
]

pesos = [
    2, 1, 3, 3,   # Gestión
    3, 2, 3, 3,   # Equipos
    3, 3, 2, 3,   # Backups
    3, 2, 2, 3    # Redes
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
        puntaje_max = sum(pesos)
        resultados = []
        idx = 0
        for segmento, preguntas in segmentos:
            for pregunta in preguntas:
                respuesta = respuestas.get(pregunta, "")
                try:
                    valor = opciones[idx].index(respuesta)
                    if valor == 0:
                        puntaje_total += pesos[idx]
                    elif valor == 1:
                        puntaje_total += pesos[idx] * 0.66
                    elif valor == 2:
                        puntaje_total += pesos[idx] * 0.33
                except:
                    pass
                resultados.append((pregunta, respuesta))
                idx += 1
        porcentaje = int((puntaje_total / puntaje_max) * 100)

        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in resultados])

        msg = Message("Resultados Evaluación Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=resultados, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)
