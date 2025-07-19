from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos y datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Tienen políticas documentadas de seguridad?", ["Sí, completas", "Parciales", "Borrador", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No seguro", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, política y actualización programada", "Sí, pero inconsistente", "No realmente", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Actualizaciones de sistema operativo y software son automáticas?", ["Sí, automatizadas", "Manual regular", "Irregular", "No"]),
        ("¿Contraseñas son fuertes y únicas?", ["Sí, política y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban periódicamente la restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
    ])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = dict(request.form)
        puntaje = sum(3 - int(respuestas[k]) for k in respuestas if k.startswith("q"))
        max_puntaje = len([p for s in segmentos for p in s[1]]) * 3
        porcentaje = round(100 * puntaje / max_puntaje)

        if porcentaje >= 80:
            concepto = "Postura robusta, siga mejorando."
        elif porcentaje >= 60:
            concepto = "Aceptable, pero con áreas por fortalecer."
        elif porcentaje >= 40:
            concepto = "Riesgosa, tome medidas cuanto antes."
        else:
            concepto = "Crítica, necesita intervención urgente."

        return render_template("resultados.html",
                               respuestas=respuestas,
                               segmentos=segmentos,
                               porcentaje=porcentaje,
                               concepto=concepto)
    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
