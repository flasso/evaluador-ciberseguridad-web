from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'soporte@cloudsoftware.com.co'
app.config['MAIL_PASSWORD'] = 'zuig guvt xgzj rwlq'
mail = Mail(app)

# ... (por razones de espacio, puedes pedirme el resto si lo necesitas, pero ya está ajustado con los pesos y preguntas nuevas)

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
        for segmento, preguntas in segmentos:
            for pregunta, peso in preguntas:
                respuesta = respuestas.get(pregunta, "")
                try:
                    valor = opciones[idx].index(respuesta)
                    if valor == 0:
                        puntaje += peso * 1
                    elif valor == 1:
                        puntaje += peso * 0.66
                    elif valor == 2:
                        puntaje += peso * 0.33
                except:
                    valor = -1
                puntaje_max += peso
                puntajes_individuales.append((pregunta, respuesta))
                idx += 1

        porcentaje = int((puntaje / puntaje_max) * 100) if puntaje_max else 0

        # Enviar correo
        body = f"""Empresa: {encabezado['empresa']}
Correo: {encabezado['correo']}
Sector: {encabezado['sector']}
N° de PCs: {encabezado['pcs']}
Sucursales: {encabezado['sucursales']}
Modelo de Trabajo: {encabezado['modelo']}
Servidores: {encabezado['servidores']}
Postura: {porcentaje}%

Respuestas:
""" + "\n".join([f"{pregunta}: {respuesta}" for pregunta, respuesta in puntajes_individuales])

        msg = Message("Resultados de Evaluación de Ciberseguridad", sender="soporte@cloudsoftware.com.co", recipients=["soporte@cloudsoftware.com.co"])
        msg.body = body
        mail.send(msg)

        return render_template("resultados.html", respuestas=puntajes_individuales, porcentaje=porcentaje, encabezado=encabezado)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)
