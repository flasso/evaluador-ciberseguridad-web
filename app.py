from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import logging

app = Flask(__name__)

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# Opciones por pregunta
opciones = [
    ['Dedicado y certificado', 'Interno no exclusivo', 'Proveedor externo', 'Ninguno'],  # TI
    ['Sí, con alertas y reportes automáticos', 'Sí, manualmente', 'Solo cuando hay problemas', 'No'],
    ['Sí, actualizado mensualmente', 'Sí, pero con retrasos', 'Parcial', 'No'],
    ['Sí, con controles definidos', 'Solo antivirus', 'Lo maneja proveedor', 'No tienen'],
    ['Sí, con doble autenticación (MFA)', 'Contraseñas fuertes', 'Contraseñas básicas', 'Sin política'],
    ['Sí, red separada y cifrada', 'Solo clave segura', 'Compartida con clientes', 'Abierta'],
    ['Sí, con backup diario probado', 'Backup semanal', 'Backup sin prueba', 'No hacen respaldo'],
    ['Sí, se hacen pruebas de recuperación', 'Solo respaldan', 'No han probado nunca', 'No saben'],
    ['Sí, cada mes', 'Cada semestre', 'Una vez al año', 'Nunca'],
    ['Sí, tienen protocolo y responsable', 'Hay una guía básica', 'Solo reacción espontánea', 'No saben qué hacer'],
    ['Sí, con monitoreo remoto y soporte', 'Solo soporte en sitio', 'Uso Team/AnyDesk sin control', 'Ninguno'],
    ['Sí, con parches automáticos', 'Solo críticas', 'Depende del proveedor', 'No actualizan'],
    ['Antivirus con EDR', 'Antivirus tradicional', 'Solo Windows Defender', 'No tiene'],
    ['Sí, al menos cada 6 meses', 'Una vez al año', 'Solo nuevo personal', 'Nunca'],
    ['Sí, reciben formación y simulacros', 'Capacitación básica', 'Solo charlas internas', 'Nunca'],
    ['Sí, hacen seguimiento centralizado', 'Hay revisión periódica', 'Revisión solo ante fallas', 'No monitorean'],
    ['Propios en oficina', 'Arrendados en datacenter', 'Mixto', 'No tienen']
]

# Pesos por pregunta (según importancia)
pesos = [2, 2, 1, 2, 2, 2, 3, 3, 2, 3, 2, 2, 3, 2, 3, 2, 2]

# Segmentos
segmentos = [
    ("Gestión de TI", [opciones[0]]),
    ("Inventario y monitoreo", [opciones[1], opciones[2]]),
    ("Controles y políticas", [opciones[3], opciones[4], opciones[5]]),
    ("Respaldos y recuperación", [opciones[6], opciones[7]]),
    ("Cultura de seguridad", [opciones[8], opciones[9], opciones[13], opciones[14]]),
    ("Infraestructura", [opciones[10], opciones[11], opciones[12], opciones[15], opciones[16]])
]

@app.route('/')
def intro():
    return render_template("intro.html")

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)
        encabezado = {k: respuestas.pop(k) for k in ['empresa', 'correo', 'sector', 'pcs', 'sucursales', 'modelo', 'servidores']}
        
        puntaje = 0
        puntaje_max = 0
        puntajes_individuales = []
        idx = 0

        for grupo in opciones:
            pregunta_texto = list(respuestas.keys())[idx]
            respuesta_usuario = respuestas.get(pregunta_texto, '')
            try:
                pos = grupo.index(respuesta_usuario)
                if pos == 0:
                    puntaje += pesos[idx] * 1
                elif pos == 1:
                    puntaje += pesos[idx] * 0.66
                elif pos == 2:
                    puntaje += pesos[idx] * 0.33
                # pos 3 (peor): 0 puntos
            except:
                pass
            puntaje_max += pesos[idx]
            puntajes_individuales.append((pregunta_texto, respuesta_usuario))
            idx += 1

        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        # Enviar correo
        cuerpo = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{p}: {r}" for p, r in puntajes_individuales])

        msg = Message("Resultados Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = cuerpo
        mail.send(msg)

        return render_template("resultados.html", respuestas=puntajes_individuales, porcentaje=porcentaje, encabezado=encabezado)

    return render_template("index.html", segmentos=segmentos, opciones=opciones)

# Ejecutar para Render
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)
