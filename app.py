from flask import Flask, render_template, request

app = Flask(__name__)

# Definición de las preguntas segmentadas
secciones = [
    {
        "titulo": "Gestión y Visibilidad",
        "preguntas": [
            "¿Su empresa cuenta con un responsable de TI?",
            "¿Se monitorea la seguridad periódicamente?",
            "¿Tiene inventario actualizado de equipos y software?"
        ]
    },
    {
        "titulo": "Protección de Red y Perímetro",
        "preguntas": [
            "¿Cuenta con un firewall de hardware o UTM?",
            "¿El firewall está bien configurado y gestionado?",
            "¿La red Wi-Fi está aislada para invitados?"
        ]
    },
    {
        "titulo": "Protección de Dispositivos y Datos",
        "preguntas": [
            "¿Todos los equipos tienen antivirus con EDR?",
            "¿Las actualizaciones de sistema son automáticas?",
            "¿Las contraseñas cumplen con políticas fuertes?",
            "¿Se usa autenticación multifactor (MFA)?"
        ]
    },
    {
        "titulo": "Respaldo y Recuperación",
        "preguntas": [
            "¿Realiza copias de seguridad diarias?",
            "¿Prueba regularmente sus respaldos?",
            "¿Cuenta con copias offline o inmutables?"
        ]
    },
    {
        "titulo": "Concientización y Respuesta a Incidentes",
        "preguntas": [
            "¿Capacita al personal sobre phishing?",
            "¿Existe un canal para reportar incidentes?",
            "¿Tiene plan de respuesta a incidentes?"
        ]
    }
]

opciones = [
    ("Sí, completamente", 4),
    ("Parcialmente", 2),
    ("No", 0),
    ("No sé", 1)
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        empresa = request.form.get("empresa")
        ciudad = request.form.get("ciudad")
        pais = request.form.get("pais")

        respuestas = {}
        puntajes = {}
        total_puntos = 0
        total_max = 0

        for seccion in secciones:
            sec_puntos = 0
            sec_max = len(seccion["preguntas"]) * 4
            for pregunta in seccion["preguntas"]:
                valor = int(request.form.get(pregunta, 0))
                respuestas[pregunta] = valor
                sec_puntos += valor
                total_puntos += valor
            puntajes[seccion["titulo"]] = (sec_puntos, sec_max)
            total_max += sec_max

        porcentaje = round((total_puntos / total_max) * 100)

        # Tabla de referencia y concepto
        if porcentaje >= 80:
            concepto = "Su postura de ciberseguridad es ROBUSTA. Mantenga las buenas prácticas."
        elif porcentaje >= 60:
            concepto = "Su postura es BUENA, pero aún hay oportunidades claras de mejora."
        elif porcentaje >= 40:
            concepto = "Su postura es DÉBIL. Se recomienda tomar medidas urgentes."
        else:
            concepto = "Su postura es CRÍTICA. Requiere intervención inmediata de un especialista."

        return render_template("resultados.html", nombre=nombre, empresa=empresa,
                               ciudad=ciudad, pais=pais,
                               porcentaje=porcentaje, concepto=concepto,
                               puntajes=puntajes, secciones=secciones,
                               respuestas=respuestas, opciones=opciones)

    return render_template("index.html", secciones=secciones, opciones=opciones)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

