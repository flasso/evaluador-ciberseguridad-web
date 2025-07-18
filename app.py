from flask import Flask, render_template, request
app = Flask(__name__)

# Segmentos y preguntas
PREGUNTAS = [
    ("Información General", [
        ("¿Nombre de la empresa?", []),
        ("¿Nombre del contacto?", []),
        ("¿Correo electrónico?", []),
        ("¿Sector de la empresa?", ["Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otros"]),
        ("¿Ciudad?", []),
        ("¿País?", ["Colombia", "Otro"])
    ]),
    ("Infraestructura y Seguridad", [
        ("¿Cuenta con firewall de red?", ["Sí, bien configurado", "Sí, pero no sé su estado", "No tengo firewall", "No sé"]),
        ("¿Revisa periódicamente la configuración del firewall?", ["Sí, regularmente", "Sí, ocasionalmente", "No", "No tengo firewall"]),
        ("¿Cuenta con antivirus con EDR en todos los equipos?", ["Sí, todos", "Parcialmente", "No", "No sé"]),
        ("¿La red WiFi tiene contraseña fuerte y separada por invitados?", ["Sí, ambas cosas", "Solo contraseña fuerte", "No", "No sé"])
    ]),
    ("Gestión y Continuidad", [
        ("¿Tiene un responsable de TI o ciberseguridad?", ["Sí, interno", "Sí, externo (MSSP)", "No", "No sé"]),
        ("¿Cuenta con respaldos periódicos probados?", ["Sí, bien gestionados", "A veces", "No", "No sé"]),
        ("¿Tiene plan de continuidad y recuperación ante desastres?", ["Sí", "Parcial", "No", "No sé"]),
        ("¿Capacita regularmente al personal en ciberseguridad?", ["Sí", "A veces", "No", "No sé"])
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {}
        for k, v in request.form.items():
            respuestas[k] = v

        # Cálculo básico de puntaje por ahora
        puntaje = 0
        max_puntaje = 0
        for segmento, preguntas in PREGUNTAS:
            for idx, (texto, opciones) in enumerate(preguntas):
                if opciones:
                    max_puntaje += 3
                    valor = respuestas.get(f"p_{segmento}_{idx}", "")
                    if valor == "0": puntaje += 3
                    elif valor == "1": puntaje += 2
                    elif valor == "2": puntaje += 1

        porcentaje = (puntaje / max_puntaje) * 100 if max_puntaje else 0
        return render_template("resultados.html", respuestas=respuestas, porcentaje=porcentaje, preguntas=PREGUNTAS)

    return render_template("index.html", preguntas=PREGUNTAS)
