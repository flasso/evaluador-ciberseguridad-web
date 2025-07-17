
from flask import Flask, render_template, request

app = Flask(__name__)

# Preguntas organizadas
PREGUNTAS = [
    {"id": "responsable_ti", "texto": "¿Tu empresa tiene un responsable claro y competente en TI o ciberseguridad?", "opciones": ["Sí, especializado", "Sí, pero no especializado", "No", "No sé"]},
    {"id": "monitoreo", "texto": "¿Se realiza monitoreo regular de la seguridad (logs, accesos, antivirus)?", "opciones": ["Sí, diario", "Sí, semanal", "No", "No sé"]},
    {"id": "inventario", "texto": "¿Existe un inventario actualizado de equipos, software y datos críticos?", "opciones": ["Sí, actualizado", "Sí, pero desactualizado", "No", "No sé"]},
    {"id": "firewall", "texto": "¿La empresa tiene un firewall dedicado de hardware o UTM para proteger la red?", "opciones": ["Sí, bien gestionado", "Sí, pero mal gestionado", "No", "No sé"]},
    {"id": "firewall_gestion", "texto": "¿Quién configura y monitorea el firewall?", "opciones": ["Especialista en ciberseguridad", "TI interno no especializado", "Proveedor externo no especializado", "No tengo firewall"]},
    {"id": "wifi", "texto": "¿La red Wi-Fi empresarial está aislada para invitados y protegida?", "opciones": ["Sí, aislada y segura", "Sí, pero débil", "No", "No sé"]},
    {"id": "antivirus", "texto": "¿Todos los equipos tienen antivirus empresarial con EDR?", "opciones": ["Sí, con EDR", "Sí, sin EDR", "Básico o gratuito", "No"]},
    {"id": "actualizaciones", "texto": "¿Las actualizaciones de sistema y software son automáticas y regulares?", "opciones": ["Sí, automáticas", "Sí, manuales", "No", "No sé"]},
    {"id": "contrasenas", "texto": "¿Se usan contraseñas fuertes y gestores de contraseñas?", "opciones": ["Sí, estrictas con gestor", "Sí, pero inconsistentes", "No", "No sé"]},
    {"id": "mfa", "texto": "¿Las cuentas críticas tienen autenticación multifactor (MFA)?", "opciones": ["Sí, en todas", "Sí, en algunas", "No", "No sé"]},
    {"id": "backup_frecuencia", "texto": "¿Se hacen backups diarios o más frecuentes?", "opciones": ["Sí, diarios", "Semanal", "Mensual", "No"]},
    {"id": "backup_pruebas", "texto": "¿Se prueban las copias de seguridad para su restauración?", "opciones": ["Sí, regularmente", "Ocasionalmente", "No", "No sé"]},
    {"id": "backup_offline", "texto": "¿Se guarda una copia aislada u offline?", "opciones": ["Sí", "No", "No sé", "No aplica"]},
    {"id": "backup_responsable", "texto": "¿Existe un responsable de los respaldos y recuperación?", "opciones": ["Sí, designado", "No claramente", "No", "No sé"]},
    {"id": "capacitacion", "texto": "¿Los empleados reciben capacitación regular en ciberseguridad?", "opciones": ["Sí, anual", "Ocasional", "Nunca", "No sé"]},
    {"id": "reporte", "texto": "¿Los empleados saben cómo reportar incidentes?", "opciones": ["Sí, claro", "Sí, informal", "No", "No sé"]},
    {"id": "plan_incidentes", "texto": "¿Existe un plan documentado y probado de respuesta a incidentes?", "opciones": ["Sí, probado", "Sí, sin probar", "No", "No sé"]}
]

REFERENCIA = [
    ("80% - 100%", "Postura Robusta", "Tu empresa demuestra un alto nivel de ciberseguridad. Mantén las buenas prácticas y sigue mejorando."),
    ("60% - 79%", "Base Buena", "Tienes fundamentos sólidos, pero hay áreas claras para mejorar."),
    ("30% - 59%", "Riesgo Elevado", "Tu empresa está en riesgo significativo. Es importante tomar acción rápidamente."),
    ("0% - 29%", "Riesgo Crítico", "Tu empresa es altamente vulnerable. Se requieren acciones urgentes.")
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        datos = request.form
        respuestas = {k: datos.get(k) for k in datos if k.startswith("p_")}
        empresa = datos.get("empresa")
        contacto = datos.get("contacto")
        email = datos.get("email")
        sector = datos.get("sector")
        ciudad = datos.get("ciudad")
        pais = datos.get("pais")

        puntaje = sum(1 for v in respuestas.values() if v in ["Sí, especializado", "Sí, diario", "Sí, actualizado", "Sí, bien gestionado", "Especialista en ciberseguridad", "Sí, aislada y segura", "Sí, con EDR", "Sí, automáticas", "Sí, estrictas con gestor", "Sí, en todas", "Sí, diarios", "Sí, regularmente", "Sí", "Sí, designado", "Sí, anual", "Sí, claro", "Sí, probado"])
        porcentaje = round(puntaje / 17 * 100)

        if porcentaje >= 80:
            nivel = REFERENCIA[0]
        elif porcentaje >= 60:
            nivel = REFERENCIA[1]
        elif porcentaje >= 30:
            nivel = REFERENCIA[2]
        else:
            nivel = REFERENCIA[3]

        return render_template("resultados.html", empresa=empresa, porcentaje=porcentaje, nivel=nivel, respuestas=respuestas)

    return render_template("index.html", preguntas=PREGUNTAS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

