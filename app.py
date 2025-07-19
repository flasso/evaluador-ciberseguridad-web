from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No seguro", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Contraseñas son seguras y se actualizan periódicamente?", ["Sí, política estricta", "Sí, pero informal", "No", "No sabe"]),
        ("¿Actualizaciones de sistema/software son automáticas?", ["Sí, automatizadas", "Manual regular", "Irregular", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = dict(request.form)
        total_preguntas = sum(len(s[1]) for s in segmentos)
        puntaje = 0
        resultados = []

        for s_idx, (_, preguntas) in enumerate(segmentos):
            for p_idx, (pregunta, opciones) in enumerate(preguntas):
                key = f"q{s_idx}_{p_idx}"
                respuesta = respuestas.get(key)
                resultados.append((pregunta, respuesta))
                if respuesta == opciones[0]:
                    puntaje += 1
                elif respuesta == opciones[1]:
                    puntaje += 0.75
                elif respuesta == opciones[2]:
                    puntaje += 0.5
                # peor opción = 0

        porcentaje = round((puntaje / total_preguntas) * 100, 1)

        return render_template("resultados.html", resultados=resultados, porcentaje=porcentaje)

    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
