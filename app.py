from flask import Flask, render_template, request

app = Flask(__name__)

# Segmentos y preguntas
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida", "Sí, pero informal", "No actualizan", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacitan regularmente al personal en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ])
]

# Ponderación: 3 → óptimo … 0 → crítico
valores = [3, 2, 1, 0]

@app.route("/", methods=["GET"])
def intro():
    return render_template("intro.html")

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():
    if request.method == "POST":
        respuestas = dict(request.form)
        puntaje_total = 0
        puntaje_maximo = 0
        recomendaciones = []

        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                respuesta = respuestas.get(pregunta)
                if respuesta in opciones:
                    idx = opciones.index(respuesta)
                    puntos = valores[idx]
                    puntaje_total += puntos
                    puntaje_maximo += 3
                    if puntos <=1:
                        recomendaciones.append(f"🔷 Mejore: {pregunta} (actual: {respuesta})")

        porcentaje = round((puntaje_total / puntaje_maximo) * 100) if puntaje_maximo > 0 else 0

        # Añadir consejo final
        recomendaciones.append("💡 Recomendación: considere contar con un proveedor MSP que le apoye en la gestión e implementación de las mejoras necesarias.")

        return render_template("resultados.html",
                               respuestas=respuestas,
                               porcentaje=porcentaje,
                               recomendaciones=recomendaciones)

    return render_template("index.html", segmentos=segmentos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
