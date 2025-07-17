
from flask import Flask, render_template, request

app = Flask(__name__)

CATEGORIAS = [
    (0, 30, "RIESGO CRÍTICO"),
    (31, 60, "RIESGO ELEVADO"),
    (61, 80, "BUENA BASE"),
    (81, 100, "POSTURA ROBUSTA")
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        respuestas = request.form.to_dict()
        puntaje = 0
        max_puntaje = 0
        recomendaciones = []

        puntajes_preguntas = {
            # Gestión y visibilidad
            "personal_ti": {"Sí": 5, "No": 0, "No sé": 1},
            "responsable_backups": {"Sí": 5, "No": 0, "No sé": 1},

            # Protección de red
            "firewall": {"Sí": 5, "No tengo firewall": 0, "No sé": 1, "No reviso configuración": 2},

            # Protección de dispositivos
            "software_original": {"Sí": 5, "No": 0, "No sé": 1},
            "actualizaciones": {"Automáticas": 5, "Manuales": 3, "Nunca": 0, "No sé": 1},
            "mfa": {"Sí": 5, "No": 0, "No sé": 1},

            # Respaldo
            "backups": {"Diario": 5, "Semanal": 3, "Nunca": 0, "No sé": 1},

            # Concientización
            "capacitacion": {"Sí": 5, "No": 0, "No sé": 1},
        }

        for key, valor in respuestas.items():
            if key in puntajes_preguntas:
                puntaje += puntajes_preguntas[key].get(valor, 0)
                max_puntaje += 5

        porcentaje = (puntaje / max_puntaje) * 100 if max_puntaje > 0 else 0
        categoria = next((c for min_p, max_p, c in CATEGORIAS if min_p <= porcentaje <= max_p), "N/A")

        if categoria in ["RIESGO CRÍTICO", "RIESGO ELEVADO"]:
            recomendaciones.append("Asigne un responsable claro de TI y de copias de seguridad.")
            recomendaciones.append("Implemente un firewall bien configurado y supervisado.")
            recomendaciones.append("Asegúrese de que todos los equipos tengan software original y actualizado.")
            recomendaciones.append("Realice capacitaciones periódicas al personal.")
            recomendaciones.append("Configure respaldos diarios y verifique su restauración.")

        return render_template(
            "resultados.html",
            respuestas=respuestas,
            puntaje=int(puntaje),
            max_puntaje=int(max_puntaje),
            porcentaje=int(porcentaje),
            categoria=categoria,
            recomendaciones=recomendaciones
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
