from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No seguro", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Actualizaciones de sistema/software son automáticas?", ["Sí, automatizadas", "Manual regular", "Irregular", "No"]),
        ("¿Contraseñas son fuertes y únicas?", ["Sí, política y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
    ])
]

puntos_opciones = [5, 3, 1, 0]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = dict(request.form)
        total_puntos = 0
        max_puntos = 0
        detalle = []
        for idx, (segmento, preguntas) in enumerate(segmentos):
            for pregunta, opciones in preguntas:
                resp = respuestas.get(pregunta)
                if resp in opciones:
                    puntos = puntos_opciones[opciones.index(resp)]
                else:
                    puntos = 0
                total_puntos += puntos
                max_puntos += 5
                detalle.append((pregunta, resp, puntos))

        porcentaje = round(total_puntos / max_puntos * 100, 1)
        if porcentaje >= 80:
            concepto = "Postura Robusta"
        elif porcentaje >= 60:
            concepto = "Aceptable"
        elif porcentaje >= 40:
            concepto = "Riesgosa"
        else:
            concepto = "Crítica"

        recomendaciones = [
            "Fortalezca las áreas más débiles detectadas.",
            "Implemente autenticación multifactor.",
            "Considere contratar un MSSP si no tiene personal experto.",
            "Pruebe y automatice sus respaldos.",
            "Capacite a su personal regularmente."
        ]

        return render_template("resultados.html", detalle=detalle, porcentaje=porcentaje, concepto=concepto, recomendaciones=recomendaciones)

    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

