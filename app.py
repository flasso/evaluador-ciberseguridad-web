from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        "¿Quién es el responsable de TI/ciberseguridad?",
        "¿Monitorean la seguridad regularmente?",
        "¿Tienen inventario actualizado de equipos/datos?"
    ]),
    ("Protección de Red", [
        "¿Tienen firewall de hardware o UTM?",
        "¿Quién gestiona el firewall?",
        "¿Wi-Fi está segura y separada para invitados?"
    ]),
    ("Protección de Dispositivos", [
        "¿Tienen antivirus/EDR en todos los equipos?",
        "¿Contraseñas son seguras y se actualizan periódicamente?",
        "¿Actualizaciones de sistema/software son automáticas?",
        "¿Tienen MFA activada en cuentas críticas?"
    ]),
    ("Respaldo y Conciencia", [
        "¿Respaldan datos críticos a diario?",
        "¿Prueban restauración de respaldos?",
        "¿Tienen personal encargado de sistemas?",
        "¿Tienen responsable de las copias de seguridad?"
    ])
]

opciones = [
    "Opción 1", "Opción 2", "Opción 3", "Opción 4"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = request.form.to_dict()
        puntaje = 0
        total = 0

        for k, v in respuestas.items():
            if k.startswith("q"):
                try:
                    puntaje += int(v)
                except:
                    pass
                total += 3  # puntaje máximo por pregunta

        porcentaje = int((puntaje / total) * 100) if total else 0

        if porcentaje >= 80:
            concepto = "Postura Robusta"
        elif porcentaje >= 60:
            concepto = "Postura Aceptable"
        elif porcentaje >= 40:
            concepto = "Postura Riesgosa"
        else:
            concepto = "Postura Crítica"

        return render_template("resultados.html", respuestas=respuestas, segmentos=segmentos,
                               porcentaje=porcentaje, concepto=concepto)
    return render_template("index.html", segmentos=segmentos, opciones=opciones)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

