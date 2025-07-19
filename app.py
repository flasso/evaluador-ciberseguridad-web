@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        datos = dict(request.form)
        respuestas = {k: v for k, v in datos.items() if k.startswith("pregunta")}

        # Calcular puntaje
        puntaje_total = 0
        max_puntaje = 0
        recomendaciones = []

        for key, respuesta in respuestas.items():
            if respuesta == "Dedicado y certificado" or respuesta.startswith("Sí"):
                puntaje_total += 5
            elif respuesta == "Interno no exclusivo" or "Manual" in respuesta or "Inconsistente" in respuesta:
                puntaje_total += 3
            elif respuesta == "Proveedor externo" or "Gratis" in respuesta:
                puntaje_total += 2
            else:
                puntaje_total += 0
            max_puntaje += 5

            if respuesta in ["No", "No seguro", "No hay firewall", "No sabe"]:
                recomendaciones.append(f"Mejorar: {key} — respuesta actual: {respuesta}")

        porcentaje = round((puntaje_total / max_puntaje) * 100)

        if porcentaje < 40:
            concepto = "Crítica"
        elif porcentaje < 60:
            concepto = "Riesgosa"
        elif porcentaje < 80:
            concepto = "Aceptable"
        else:
            concepto = "Robusta"

        return render_template(
            "resultados.html",
            datos=datos,
            respuestas=respuestas,
            porcentaje=porcentaje,
            concepto=concepto,
            recomendaciones=recomendaciones,
        )

    return render_template("index.html", segmentos=segmentos)
