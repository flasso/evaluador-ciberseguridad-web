from flask import Flask, render_template, request
app = Flask(__name__)

PREGUNTAS = [
    # Información general
    {"id": "empresa", "texto": "Nombre de la empresa", "tipo": "texto"},
    {"id": "contacto", "texto": "Persona de contacto", "tipo": "texto"},
    {"id": "email", "texto": "Correo electrónico", "tipo": "texto"},
    {"id": "ciudad", "texto": "Ciudad", "tipo": "texto"},
    {"id": "pais", "texto": "País", "tipo": "texto", "valor_defecto": "Colombia"},
    {"id": "sector", "texto": "Sector", "tipo": "select", "opciones": [
        "Servicios", "Manufactura", "Tecnología", "Alimentos", "Legales", "Contables", "Distribución", "Otros"
    ]},

    # Grupo 1: Gestión y visibilidad
    {"id": "responsable_ti", "texto": "¿Su empresa cuenta con un responsable de TI/ciberseguridad?", "tipo": "select", "opciones": [
        "Sí, interno dedicado", "Sí, interno parcial", "Proveedor externo", "No"
    ]},
    {"id": "inventario_activos", "texto": "¿Llevan inventario actualizado de dispositivos y sistemas?", "tipo": "select", "opciones": [
        "Sí", "Parcial", "No", "No sé"
    ]},

    # Grupo 2: Protección perimetral
    {"id": "firewall", "texto": "¿Cuentan con un firewall para proteger la red?", "tipo": "select", "opciones": [
        "Sí, administrado", "Sí, pero sin gestión", "No", "No sé"
    ]},
    {"id": "revision_firewall", "texto": "¿Revisan periódicamente las configuraciones y registros del firewall?", "tipo": "select", "opciones": [
        "Sí, regularmente", "Ocasionalmente", "No", "No tengo firewall"
    ]},

    # Grupo 3: Protección de dispositivos
    {"id": "antivirus", "texto": "¿Tienen antivirus con EDR instalado en todos los equipos?", "tipo": "select", "opciones": [
        "Sí, con EDR", "Sí, básico", "Parcial", "No"
    ]},
    {"id": "actualizaciones", "texto": "¿Actualizan el sistema operativo y aplicaciones regularmente?", "tipo": "select", "opciones": [
        "Automáticas", "Manuales regulares", "Irregular", "No"
    ]},

    # Grupo 4: Respaldo y recuperación
    {"id": "copias", "texto": "¿Realizan copias de seguridad de la información crítica?", "tipo": "select", "opciones": [
        "Sí, diarias y probadas", "Sí, semanales", "Ocasional", "No"
    ]},
    {"id": "copias_offline", "texto": "¿Mantienen copias de seguridad offline o inmutables?", "tipo": "select", "opciones": [
        "Sí", "Parcial", "No", "No sé"
    ]},

    # Grupo 5: Concientización
    {"id": "capacitacion", "texto": "¿Capacitan a sus empleados sobre phishing y seguridad?", "tipo": "select", "opciones": [
        "Sí, anual", "Sí, ocasional", "No", "No sé"
    ]},
    {"id": "mfa", "texto": "¿Usan autenticación multifactor (MFA) en las cuentas críticas?", "tipo": "select", "opciones": [
        "Sí, en todas", "Sí, en algunas", "No", "No sé"
    ]}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = {k: v for k, v in request.form.items()}
        puntaje = calcular_puntaje(respuestas)
        categoria, recomendaciones = determinar_postura(puntaje)
        return render_template("resultados.html", respuestas=respuestas, puntaje=puntaje,
                               categoria=categoria, recomendaciones=recomendaciones)
    return render_template("index.html", preguntas=PREGUNTAS)

def calcular_puntaje(respuestas):
    puntaje = 0
    for k, v in respuestas.items():
        if v.startswith("Sí"):
            puntaje += 3
        elif v in ["Automáticas", "Sí, anual", "Sí, diarias y probadas", "Sí, con EDR", "Sí, administrado"]:
            puntaje += 4
        elif v in ["Parcial", "Ocasional", "Sí, en algunas"]:
            puntaje += 2
    return puntaje

def determinar_postura(puntaje):
    if puntaje >= 50:
        return "Alta", [
            "Mantenga su nivel actual y realice auditorías periódicas.",
            "Siga reforzando la cultura de ciberseguridad en su personal."
        ]
    elif puntaje >= 30:
        return "Media", [
            "Mejore los controles técnicos y capacite más a su personal.",
            "Implemente políticas y procedimientos claros."
        ]
    else:
        return "Baja", [
            "Considere un plan integral urgente de ciberseguridad.",
            "Busque apoyo especializado para fortalecer su postura."
        ]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
