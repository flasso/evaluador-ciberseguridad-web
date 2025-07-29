from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Segmentos y preguntas con sus opciones asociadas directamente
segmentos_con_opciones = [
    ("Gestión de TI", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"])
    ]),
    ("Inventario y monitoreo", [
        ("¿Utilizan herramientas de monitoreo del estado de salud de los equipos?", ["Sí, con alertas y reportes automáticos", "Sí, manualmente", "Solo cuando hay problemas", "No"]),
        ("¿Tienen inventario actualizado de equipos y datos?", ["Sí, actualizado mensualmente", "Sí, pero con retrasos", "Parcial", "No"])
    ]),
    ("Controles y políticas", [
        ("¿Tienen políticas y controles de ciberseguridad documentados?", ["Sí, con controles definidos", "Solo antivirus", "Lo maneja proveedor", "No tienen"]),
        ("¿Utilizan autenticación multifactor (MFA)?", ["Sí, con doble autenticación (MFA)", "Contraseñas fuertes", "Contraseñas básicas", "Sin política"]),
        ("¿Tienen Wi-Fi separado para invitados/clientes?", ["Sí, red separada y cifrada", "Solo clave segura", "Compartida con clientes", "Abierta"])
    ]),
    ("Respaldos y recuperación", [
        ("¿Hacen respaldos periódicos?", ["Sí, con backup diario probado", "Backup semanal", "Backup sin prueba", "No hacen respaldo"]),
        ("¿Han probado la restauración de respaldos?", ["Sí, se hacen pruebas de recuperación", "Solo respaldan", "No han probado nunca", "No saben"])
    ]),
    ("Cultura de seguridad", [
        ("¿Capacitan al personal en ciberseguridad?", ["Sí, cada mes", "Cada semestre", "Una vez al año", "Nunca"]),
        ("¿Tienen un plan de respuesta a incidentos?", ["Sí, tienen protocolo y responsable", "Hay una guía básica", "Solo reacción espontánea", "No saben qué hacer"]),
        ("¿Hacen simulacros o pruebas de seguridad?", ["Sí, al menos cada 6 meses", "Una vez al año", "Solo nuevo personal", "Nunca"]),
        ("¿Incluyen la ciberseguridad en inducción o entrenamiento inicial?", ["Sí, reciben formación y simulacros", "Capacitación básica", "Solo charlas internas", "Nunca"])
    ]),
    ("Infraestructura", [
        ("¿Cómo gestionan de manera remota los equipos?", ["Sí, con monitoreo remoto y soporte", "Solo soporte en sitio", "Uso Team/AnyDesk sin control", "Ninguno"]),
        ("¿Aplican parches y actualizaciones de seguridad?", ["Sí, con parches automáticos", "Solo críticas", "Depende del proveedor", "No actualizan"]),
        ("¿Tienen solución de antivirus o EDR?", ["Antivirus con EDR", "Antivirus tradicional", "Solo Windows Defender", "No tiene"]),
        ("¿Utilizan herramientas de monitoreo del entorno?", ["Sí, hacen seguimiento centralizado", "Hay revisión periódica", "Revisión solo ante fallas", "No monitorean"])
    ])
]

# Crear un mapeo de preguntas a sus opciones para la lógica de POST y pesos
preguntas_y_opciones_planas = []
for _, preguntas_del_segmento in segmentos_con_opciones:
    for pregunta_texto, opciones_pregunta in preguntas_del_segmento:
        preguntas_y_opciones_planas.append((pregunta_texto, opciones_pregunta))

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
        pesos = {
            6: 5,  # ¿Hacen respaldos periódicos? (índice global 6)
            7: 5,  # ¿Han probado la restauración de respaldos? (índice global 7)
            9: 4,  # ¿Tienen un plan de respuesta a incidentes? (índice global 9)
            13: 5, # ¿Aplican parches y actualizaciones de seguridad? (índice global 13)
            14: 5  # ¿Tienen solución de antivirus o EDR? (índice global 14)
        }

        for idx_pregunta_global, (pregunta_texto, opciones_disponibles) in enumerate(preguntas_y_opciones_planas):
            respuesta_elegida = respuestas.get(pregunta_texto, "No respondido")
            
            try:
                idx_opcion_elegida = opciones_disponibles.index(respuesta_elegida)
                
                peso_pregunta_actual = pesos.get(idx_pregunta_global, 3) 

                if idx_opcion_elegida == 0:
                    puntaje_obtenido += peso_pregunta_actual
                elif idx_opcion_elegida == 1:
                    puntaje_obtenido += peso_pregunta_actual * 0.66
                elif idx_opcion_elegida == 2:
                    puntaje_obtenido += peso_pregunta_actual * 0.33
                
                puntaje_total += peso_pregunta_actual
            except ValueError:
                pass
            
            resultado_preguntas.append((pregunta_texto, respuesta_elegida))

        porcentaje = round((puntaje_obtenido / puntaje_total) * 100) if puntaje_total else 0

        # --- INICIO: Generación de texto de sugerencias para el correo ---
        sugerencias_texto = """
---
Sugerencias y Próximos Pasos:

Basado en los resultados de su evaluación, considere las siguientes recomendaciones para mejorar la postura de ciberseguridad de su empresa:

* Identifique sus puntos débiles: Revise sus respuestas para identificar las áreas donde su empresa puede mejorar.
* Priorice las acciones críticas: Enfóquese primero en implementar controles básicos y desarrollar planes de respuesta a incidentes.
* Capacitación Continua: Invierta en formación regular para todo su personal.
* Actualización y monitoreo: Mantenga todos sus sistemas y software actualizados e implemente soluciones de monitoreo.
* Plan de recuperación: Asegúrese de que sus respaldos de información sean periódicos, seguros y probados.
"""
        # Añadir recomendación de MSP si el porcentaje es bajo
        if porcentaje < 90:
            sugerencias_texto += f"""
¡Atención! Refuerce su Ciberseguridad:
Dada su postura actual ({porcentaje}%), le recomendamos encarecidamente contar con el apoyo de una empresa especializada en ciberseguridad bajo un modelo de Servicio Gestionado (MSP). Un MSP con trayectoria y soluciones confiables puede ofrecerle monitoreo constante, gestión de amenazas, soporte experto y la implementación de controles avanzados que son cruciales para proteger su negocio de las amenazas actuales. No espere a ser un objetivo para actuar. Invertir en ciberseguridad ahora es invertir en la continuidad de su negocio.
"""
        # --- FIN: Generación de texto de sugerencias ---


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
""" + "\n".join([f"- {p}: {r}" for p, r in resultado_preguntas]) + sugerencias_texto # <-- AQUI SE AÑADE EL TEXTO DE SUGERENCIAS

        try:
            msg = Message(
                "Resultados de Evaluación de Ciberseguridad - " + encabezado['empresa'], 
                sender="soporte@cloudsoftware.com.co", 
                recipients=[encabezado['correo'], "soporte@cloudsoftware.com.co"]
            )
            msg.body = cuerpo_correo
            mail.send(msg)
        except Exception as e:
            print(f"Error al enviar correo: {e}")

        return render_template("resultados.html", respuestas=resultado_preguntas, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos_con_opciones)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)