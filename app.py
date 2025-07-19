from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"])
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No seguro", "No"])
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Actualizaciones de sistema/software son automáticas?", ["Sí, automatizadas", "Manual regular", "Irregular", "No"]),
        ("¿Contraseñas son fuertes y únicas?", ["Sí, política y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"])
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"])
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        datos = dict(request.form)
        respuestas = {k: v for k, v in datos.items() if k.startswith("pregunta")}
        puntaje = 0
        max_puntaje = len(respuestas) * 3
        for r in respuestas.values():
            puntaje += max(0, 3 - ["Dedicado y certificado", "Sí, detallado", "Sí, gestionado", "Sí, WPA3", "Sí, EDR", "Sí, automatizadas", "Sí, política y gestor", "Sí, en todas", "Sí, diario", "Sí, programada"].count(r))
        porcentaje = int(100 - (puntaje / max_puntaje) * 100)
        return render_template("resultados.html", datos=datos, respuestas=respuestas, porcentaje=porcentaje)
    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)