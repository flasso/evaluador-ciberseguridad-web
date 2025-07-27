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

segmentos = [
    ("Gestión y Planeación", [
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?",
        "¿El software y sistemas están actualizados con los últimos parches?",
        "¿Capacitan regularmente a sus empleados en ciberseguridad?",
        "¿Tienen un plan definido de respuesta ante incidentes?",
    ]),
    ("Protección de Red", [
        "¿Tienen firewall físico o UTM correctamente configurado?",
        "¿Quién gestiona el firewall/UTM?",
        "¿El Wi-Fi está segmentado y protegido?",
    ]),
    ("Accesos y autenticación", [
        "¿Utilizan contraseñas robustas y cambiadas regularmente?",
        "¿Tienen habilitada la Autenticación Multifactor (MFA)?",
    ]),
    ("Copias de Seguridad", [
        "¿Realizan respaldos diarios de su información crítica?",
        "¿Verifican periódicamente que los respaldos pueden restaurarse?",
    ]),
    ("Gestión Remota y Antivirus", [
        "¿Cómo gestionan los equipos de forma remota?",
        "¿Cuentan con antivirus con EDR en todos los equipos?",
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, monitoreo activo", "Solo alertas básicas", "Depende del usuario", "No se monitorea"],
    ["Sí, completo y actualizado", "Sí, parcial", "Obsoleto", "No tienen"],
    ["Sí, actualizados de forma automática", "Sí, manualmente", "De vez en cuando", "No se actualizan"],
    ["Sí, cada 6-12 meses", "Sí, 1 vez al año", "Solo al ingresar", "No se capacita"],
    ["Sí, con roles y responsables", "Sí, básico", "Lo estamos creando", "No tenemos plan"],
    ["Sí, configurado profesionalmente", "Sí, pero básico", "Solo software en PC", "No tienen firewall"],
    ["TI especializado", "Personal no especializado", "Proveedor externo", "Nadie lo gestiona"],
    ["Sí, con red por segmento", "Una red protegida", "Red única con contraseña", "Abierta o sin protección"],
    ["Sí, complejas y gestionadas", "Sí, pero sin política clara", "Solo algunas áreas", "Cualquiera crea su clave"],
    ["Sí, en todos los accesos", "Solo correos y VPN", "En pruebas", "No usamos MFA"],
    ["Sí, diariamente y verificado", "Sí, diariamente", "Ocasionalmente", "No se hacen"],
    ["Sí, mensualmente", "Sí, 1 vez al año", "Lo hemos hecho alguna vez", "Nunca se prueba"],
    ["Con herramientas como TeamViewer/AnyDesk", "Acceso remoto limitado", "Conexiones esporádicas", "No se gestiona remotamente"],
    ["Sí, EDR con monitoreo", "Solo antivirus básico", "Antivirus sin actualizar", "No tienen"],
]

pesos = [4, 4, 2, 5, 4, 5, 5, 3, 3, 3, 5, 5, 5, 3, 5]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        form = request.form
        encabezado = {k: form.get(k, "") for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        respuestas = []
        puntaje = 0
        total = 0

        for idx, (segmento, preguntas) in enumerate(segmentos):
            for p_idx, pregunta in enumerate(preguntas):
                respuesta = form.get(pregunta, "No respondida")
                respuestas.append((pregunta, respuesta))

                try:
                    nivel = opciones[len(respuestas)-1].index(respuesta)
                    if nivel == 0:
                        puntaje += pesos[len(respuestas)-1] * 1
                    elif nivel == 1:
                        puntaje += pesos[len(respuestas)-1] * 0.66
                    elif nivel == 2:
                        puntaje += pesos[len(respuestas)-1] * 0.33
                except:
                    pass
                total += pesos[len(respuestas)-1]

        porcentaje = int((puntaje / total) * 100) if total else 0

        # Enviar correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de trabajo: {encabezado['modelo']}
Tipo de servidores: {encabezado['servidores']}
Postura de Ciberseguridad: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in respuestas])

        msg = Message("Resultados Evaluación Ciberseguridad", sender=app.config['MAIL_USERNAME'], recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)
