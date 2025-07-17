from flask import Flask, render_template, request

app = Flask(__name__)

PREGUNTAS = [
    {"id": "q_empresa", "texto": "Nombre de la empresa"},
    {"id": "q_contacto", "texto": "Nombre del contacto"},
    {"id": "q_email", "texto": "Correo electrónico"},
    {"id": "q_sector", "texto": "Sector empresarial", "opciones": [
        "Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otro"
    ]},
    {"id": "q_ciudad", "texto": "Ciudad"},
    {"id": "q_pais", "texto": "País", "valor_defecto": "Colombia"},
    {"id": "q_personal_ti", "texto": "¿Cuenta con personal encargado de TI?", "opciones": [
        "Sí, especializado", "Sí, no especializado", "No", "No sé"
    ]},
    {"id": "q_inventario", "texto": "¿Tiene inventario actualizado de activos digitales?", "opciones": [
        "Sí, actualizado", "Sí, parcial", "No", "No sé"
    ]},
    {"id": "q_firewall", "texto": "¿Cuenta con firewall de hardware?", "opciones": [
        "Sí, bien gestionado", "Sí, pero mal gestionado", "No", "No sé"
    ]},
    {"id": "q_gestion_firewall", "texto": "¿Quién gestiona el firewall?", "opciones": [
        "Personal especializado", "Proveedor externo", "No gestionado", "No tengo firewall"
    ]},
    {"id": "q_antivirus", "texto": "¿Todos los equipos tienen antivirus con EDR?", "opciones": [
        "Sí, en todos", "Sí, en algunos", "No", "No sé"
    ]},
    {"id": "q_actualizaciones", "texto": "¿Actualizan el sistema operativo y software?", "opciones": [
        "Sí, automáticamente", "Sí, manual", "No", "No sé"
    ]},
    {"id": "q_mfa", "texto": "¿Usan autenticación multifactor (MFA) en cuentas críticas?", "opciones": [
        "Sí, en todas", "En algunas", "No", "No sé"
    ]},
    {"id": "q_backups", "texto": "¿Realizan y prueban copias de seguridad regularmente?", "opciones": [
        "Sí, probadas", "Sí, no probadas", "No", "No sé"
    ]},
    {"id": "q_plan_incidentes", "texto": "¿Tienen un plan documentado de respuesta a incidentes?", "opciones": [
        "Sí, probado", "Sí, no probado", "No", "No sé"
    ]},
    {"id": "q_capacitacion", "texto": "¿Capacitan al personal en ciberseguridad?", "opciones": [
        "Sí, regularmente", "Sí, ocasionalmente", "No", "No sé"
    ]},
    {"id": "q_monitoreo", "texto": "¿Monitorean eventos de seguridad?", "opciones": [
        "Sí, diario", "Sí, semanal", "No", "No sé"
    ]},
]

PUNTUACION_OPCIONES = {
    "Sí, especializado": 5, "Sí, actualizado": 5, "Sí, bien gestionado": 5,
    "Sí, en todos": 5, "Sí, automáticamente": 5, "Sí, en todas": 5,
    "Sí, probadas": 5, "Sí, probado": 5, "Sí, regularmente": 5, "Sí, diario": 5,
    "Sí, parcial": 3, "Sí, pero mal gestionado": 3, "Sí, en algunos": 3,
    "Sí, manual": 3, "En algunas": 3, "Sí, no probadas": 3, "Sí, no probado": 3,
    "Sí, ocasionalmente": 3, "Sí, semanal": 3,
    "No": 0, "No gestionado": 0, "No tengo firewall": 0, "No sé": 0
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {k: v for k, v in request.form.items()}
        puntuacion = sum(PUNTUACION_OPCIONES.get(v, 0) for k, v in respuestas.items() if k.startswith("q_"))
        maximo = len([p for p in PREGUNTAS if p['id'].startswith("q_") and p.get("opciones")]) * 5
        porcentaje = (puntuacion / maximo) * 100 if maximo else 0
        return render_template("resultados.html", respuestas=respuestas, preguntas=PREGUNTAS, porcentaje=porcentaje)
    return render_template("index.html", preguntas=PREGUNTAS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
