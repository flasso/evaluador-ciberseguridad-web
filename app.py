from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración para envío de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Opciones y pesos
segmentos = [
    ("Gestión", [
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Tienen inventario actualizado de equipos y datos?",
        "¿Cuentan con políticas de seguridad documentadas?",
        "¿Capacitan regularmente al personal en ciberseguridad?",
        "¿Tienen un plan de respuesta ante incidentes de ciberseguridad?",
        "¿Actualizan sus sistemas con parches de seguridad?",
        "¿Cómo gestionan el acceso remoto a los equipos?"
    ]),
    ("Protección", [
        "¿Cuentan con antivirus con EDR actualizado?",
        "¿Realizan copias de seguridad diariamente?",
        "¿Verifican periódicamente que las copias de seguridad se puedan restaurar?",
        "¿Tienen segmentación de red y WiFi para invitados?",
        "¿Tienen políticas de contraseñas seguras implementadas?",
        "¿Utilizan MFA (Autenticación Multifactor)?",
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?"
    ])
]

opciones = [
    ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"],
    ["Sí, con revisión mensual", "Sí, pero sin actualizar", "Parcialmente", "No"],
    ["Sí, documentadas y aplicadas", "Sí, pero sin seguimiento", "Borradores", "No existen"],
    ["Anualmente o más", "Ocasionalmente", "Solo al ingreso", "Nunca"],
    ["Sí, detallado y probado", "Sí, pero sin pruebas", "Básico", "No saben qué hacer"],
    ["Sí, al día", "Mensualmente", "Ocasionalmente", "No actualizan"],
    ["VPN corporativa", "Herramientas como TeamViewer/AnyDesk", "Sin control definido", "No aplican"],
    ["Sí, con consola central", "Solo antivirus básico", "Solo Windows Defender", "No tienen antivirus"],
    ["Automáticamente a diario", "Semanalmente", "Ocasionalmente", "No hacen backup"],
    ["Sí, cada mes", "De vez en cuando", "Muy rara vez", "Nunca han probado restaurar"],
    ["Sí, red segmentada y segura", "Solo red separada", "Contraseña básica", "Una sola red para todo"],
    ["Requiere longitud y cambios", "Solo longitud mínima", "Solo cambio anual", "Sin política clara"],
    ["Sí, en cuentas críticas", "Solo en algunas", "En evaluación", "No usan MFA"],
    ["Sí, con alertas y reportes", "Solo software básico", "Supervisión manual", "No se monitorean"]
]

# Pesos de cada pregunta según su criticidad
pesos = [
    1, 1, 1, 2, 3, 3, 2, 3, 3, 3, 2, 2, 3, 2
]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas_form = dict(request.form)
        encabezado = {
            "empresa": respuestas_form.pop("empresa"),
            "correo": respuestas_form.pop("correo"),
            "sector": respuestas_form.pop("sector"),
            "pcs": respuestas_form.pop("pcs"),
            "sucursales": respuestas_form.pop("sucursales"),
            "modelo": respuestas_form.pop("modelo"),
            "servidores": respuestas_form.pop("servidores")
        }

        respuestas_lista = []
        puntaje_total = 0
        puntaje_max = 0

        pregunta_idx = 0
        for segmento, preguntas in segmentos:
            for pregunta in preguntas:
                respuesta = respuestas_form.get(pregunta, "")
                respuestas_lista.append((pregunta, respuesta))
                try:
                    opcion_idx = opciones[pregunta_idx].index(respuesta)
                    if opcion_idx == 0:
                        puntaje_total += pesos[pregunta_idx] * 1
                    elif opcion_idx == 1:
                        puntaje_total += pesos[pregunta_idx] * 0.66
                    elif opcion_idx == 2:
                        puntaje_total += pesos[pregunta_idx] * 0.33
                    # respuesta 3 no suma
                except:
                    pass
                puntaje_max += pesos[pregunta_idx]
                pregunta_idx += 1

        porcentaje = int((puntaje_total / puntaje_max) * 100) if puntaje_max else 0

        # Email con resultados
        cuerpo = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in respuestas_lista])

        msg = Message("Resultado Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=respuestas_lista, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)

