from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuración de Flask-Mail
# En un entorno de producción real, estos deberían ser variables de entorno de Render
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Segmentos y preguntas
segmentos = [
    ("Gestión de TI", [
        "¿Quién es el responsable de TI/ciberseguridad?"
    ]),
    ("Inventario y monitoreo", [
        "¿Utilizan herramientas de monitoreo del estado de salud de los equipos?",
        "¿Tienen inventario actualizado de equipos y datos?"
    ]),
    ("Controles y políticas", [
        "¿Tienen políticas y controles de ciberseguridad documentados?",
        "¿Utilizan autenticación multifactor (MFA)?",
        "¿Tienen Wi-Fi separado para invitados/clientes?"
    ]),
    ("Respaldos y recuperación", [
        "¿Hacen respaldos periódicos?",
        "¿Han probado la restauración de respaldos?"
    ]),
    ("Cultura de seguridad", [
        "¿Capacitan al personal en ciberseguridad?",
        "¿Tienen un plan de respuesta a incidentes?",
        "¿Hacen simulacros o pruebas de seguridad?",
        "¿Incluyen la ciberseguridad en inducción o entrenamiento inicial?"
    ]),
    ("Infraestructura", [
        "¿Cómo gestionan de manera remota los equipos?",
        "¿Aplican parches y actualizaciones de seguridad?",
        "¿Tienen solución de antivirus o EDR?",
        "¿Utilizan herramientas de monitoreo del entorno?"
    ])
]

# Opciones por pregunta (el orden debe coincidir con el de las preguntas en 'segmentos')
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
    ["Sí, hacen seguimiento centralizado", "Hay revisión periódica", "Revisión solo ante fallas", "No monitorean"]
]

@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():
    if request.method == "POST":
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        puntaje_total = 0
        puntaje_obtenido = 0
        resultado_preguntas = []

        # Pesos personalizados para algunas preguntas clave
        # El índice corresponde al orden de la pregunta global (0-indexed)
        pesos = {
            6: 5,  # ¿Hacen respaldos periódicos?
            7: 5,  # ¿Han probado la restauración de respaldos?
            9: 4,  # ¿Tienen un plan de respuesta a incidentes?
            13: 5, # ¿Aplican parches y actualizaciones de seguridad?
            14: 5  # ¿Tienen solución de antivirus o EDR?
        }

        # Iterar sobre los segmentos y sus preguntas
        for idx_segmento, (segmento_nombre, preguntas_del_segmento) in enumerate(segmentos):
            for pregunta_texto in preguntas_del_segmento:
                respuesta_elegida = respuestas.get(pregunta_texto, "No respondido")
                
                try:
                    # El índice de `opciones` corresponde al índice global de la pregunta.
                    # `len(resultado_preguntas)` nos da ese índice porque se agrega una pregunta por cada iteración.
                    idx_opcion_elegida = opciones[len(resultado_preguntas)].index(respuesta_elegida)
                    
                    # Obtiene el peso de la pregunta actual (si está en 'pesos', si no, usa 3 por defecto)
                    peso_pregunta_actual = pesos.get(len(resultado_preguntas), 3) 

                    # Calcula el puntaje obtenido para esta pregunta
                    if idx_opcion_elegida == 0:
                        puntaje_obtenido += peso_pregunta_actual
                    elif idx_opcion_elegida == 1:
                        puntaje_obtenido += peso_pregunta_actual * 0.66
                    elif idx_opcion_elegida == 2:
                        puntaje_obtenido += peso_pregunta_actual * 0.33
                    
                    # Suma el peso máximo posible de esta pregunta al puntaje total
                    puntaje_total += peso_pregunta_actual
                except ValueError:
                    # Esto maneja el caso donde la respuesta no se encontró en las opciones (ej., pregunta no respondida)
                    pass
                
                resultado_preguntas.append((pregunta_texto, respuesta_elegida))

        porcentaje = round((puntaje_obtenido / puntaje_total) * 100) if puntaje_total else 0

        # Envío de resultados por correo
        cuerpo_correo = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}

---
Postura de Ciberseguridad: {porcentaje}%

---
Respuestas Detalladas:
""" + "\n".join([f"- {p}: {r}" for p, r in resultado_preguntas])

        try:
            # Envía el correo al usuario y a soporte
            msg = Message(
                "Resultados de Evaluación de Ciberseguridad - " + encabezado['empresa'], 
                sender="soporte@cloudsoftware.com.co", 
                recipients=[encabezado['correo'], "soporte@cloudsoftware.com.co"]
            )
            msg.body = cuerpo_correo
            mail.send(msg)
        except Exception as e:
            print(f"Error al enviar correo: {e}") # Para depuración si el correo falla en producción

        return render_template("resultados.html", respuestas=resultado_preguntas, porcentaje=porcentaje, encabezado=encabezado)

    # Si el método es GET, se renderiza el formulario de evaluación
    return render_template("index.html", segmentos=segmentos, opciones=opciones)

# Esta parte es CRUCIAL para que la aplicación funcione en Render
# Obtiene el puerto de la variable de entorno 'PORT' (establecida por Render) o usa 5000 como default.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) # 0.0.0.0 asegura que sea accesible desde cualquier IP externa