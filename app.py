from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Definición de preguntas segmentadas
preguntas = {
    "Gestión y Visibilidad": [
        ("¿Tiene personal encargado de sistemas o TI?", ["Sí, personal interno dedicado", "Sí, pero no exclusivo", "Externo (proveedor)", "No hay responsable"]),
        ("¿Monitorea regularmente eventos de seguridad?", ["Sí, diariamente", "Sí, semanalmente", "Solo cuando hay problema", "No"]),
        ("¿Tiene inventario actualizado de equipos y software?", ["Sí, completo", "Sí, parcial", "No", "No estoy seguro"]),
    ],
    "Protección de Red y Perímetro": [
        ("¿Cuenta con firewall de hardware o UTM?", ["Sí, gestionado correctamente", "Sí, pero mal configurado", "No tengo firewall", "No sé"]),
        ("¿Quién administra su firewall?", ["Personal interno", "Proveedor especializado", "Otro", "No aplica (sin firewall)"]),
        ("¿Su red Wi-Fi está segura y separada para invitados?", ["Sí, WPA2/WPA3 y separada", "Sí, solo con contraseña fuerte", "No segura o no separada", "No sé"]),
    ],
    "Protección de Dispositivos y Datos": [
        ("¿Todos los equipos tienen antivirus con EDR empresarial?", ["Sí, todos", "La mayoría", "Gratis o básico", "No"]),
        ("¿Las actualizaciones son automáticas y regulares?", ["Sí, automatizadas", "Sí, manuales", "Irregulares", "No"]),
        ("¿Las contraseñas son fuertes y únicas?", ["Sí, con política y gestor", "Sí, pero inconsistentes", "No", "No sé"]),
        ("¿Usa autenticación multifactor (MFA) en servicios críticos?", ["Sí, en todos", "En algunos", "En ninguno", "No sé"]),
    ],
    "Respaldo y Recuperación": [
        ("¿Hace copias de seguridad diarias?", ["Sí, diariamente", "Semanalmente", "Mensualmente", "Irregular o nunca"]),
        ("¿Ha probado restaurar las copias de seguridad?", ["Sí, regularmente", "Sí, ocasionalmente", "No", "No sé"]),
    ],
    "Concientización y Respuesta a Incidentes": [
        ("¿Los empleados reciben capacitación en ciberseguridad?", ["Sí, anual", "Sí, ocasional", "Nunca", "No sé"]),
        ("¿Existe un procedimiento claro para reportar incidentes?", ["Sí, claro y documentado", "Sí, informal", "No", "No sé"]),
    ]
}

recomendaciones_generales = [
    "Asigne un responsable claro de ciberseguridad o contrate un proveedor especializado.",
    "Implemente políticas de contraseñas fuertes y autenticación multifactor.",
    "Asegure su red con firewall de hardware y Wi-Fi correctamente configurados.",
    "Mantenga inventario actualizado y copias de seguridad probadas regularmente.",
    "Capacite a sus empleados y establezca un plan de respuesta a incidentes."
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {}
        for grupo, qs in preguntas.items():
            respuestas[grupo] = []
            for idx, (q, _) in enumerate(qs):
                key = f"{grupo}_{idx}"
                respuesta = request.form.get(key, "No respondida")
                respuestas[grupo].append((q, respuesta))

        # Calcular promedios por grupo y total
        puntajes = {}
        total_puntaje = 0
        total_preguntas = 0
        escala = {"Sí, personal interno dedicado": 3, "Sí, diariamente": 3, "Sí, completo": 3,
                  "Sí, gestionado correctamente": 3, "Personal interno": 3, "Sí, WPA2/WPA3 y separada": 3,
                  "Sí, todos": 3, "Sí, automatizadas": 3, "Sí, con política y gestor": 3,
                  "Sí, en todos": 3, "Sí, regularmente": 3, "Sí, anual": 3, "Sí, claro y documentado": 3,
                  "Sí, pero no exclusivo": 2, "Sí, semanalmente": 2, "Sí, parcial": 2,
                  "Sí, pero mal configurado": 2, "Proveedor especializado": 2, "Sí, solo con contraseña fuerte": 2,
                  "La mayoría": 2, "Sí, manuales": 2, "Sí, pero inconsistentes": 2,
                  "En algunos": 2, "Sí, ocasionalmente": 2, "Sí, informal": 2,
                  "Externo (proveedor)": 1, "Solo cuando hay problema": 1, "No segura o no separada": 1,
                  "Gratis o básico": 1, "Irregulares": 1, "En ninguno": 1,
                  "Otro": 1, "Semanalmente": 1, "Mensualmente": 1,
                  "Nunca": 0, "No": 0, "No aplica (sin firewall)": 0, "Irregular o nunca": 0, "No sé": 0}

        for grupo, resp in respuestas.items():
            suma = 0
            for pregunta, rpta in resp:
                suma += escala.get(rpta, 0)
            promedio = suma / len(resp) if resp else 0
            puntajes[grupo] = round(promedio, 2)
            total_puntaje += suma
            total_preguntas += len(resp)

        promedio_total = round(total_puntaje / total_preguntas, 2) if total_preguntas else 0

        # Categoría
        if promedio_total >= 2.5:
            categoria = "Postura Robusta"
            concepto = "Su organización demuestra un compromiso serio con la ciberseguridad. Mantenga la vigilancia."
        elif promedio_total >= 1.5:
            categoria = "Postura Intermedia"
            concepto = "Su organización tiene bases, pero aún con riesgos importantes. Se recomienda actuar en las áreas débiles."
        else:
            categoria = "Postura Débil"
            concepto = "Su organización es muy vulnerable. Se recomienda actuar de inmediato y buscar ayuda especializada."

        return render_template("resultados.html",
                               respuestas=respuestas,
                               puntajes=puntajes,
                               promedio_total=promedio_total,
                               categoria=categoria,
                               concepto=concepto,
                               recomendaciones=recomendaciones_generales)

    return render_template("index.html", preguntas=preguntas)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
