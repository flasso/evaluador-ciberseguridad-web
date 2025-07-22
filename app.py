from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Definición de las preguntas organizadas por segmentos
segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean la seguridad regularmente?", ["Diario/24x7", "Semanal", "Mensual", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No firewall"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ])
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = dict(request.form)

        puntaje_total = 0
        maximo_total = len(segmentos) * 3 * 3  # 3 preguntas promedio por 4 segmentos × 3 pts

        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                resp_idx = int(respuestas.get(pregunta, 0))
                puntaje_total += 3 - resp_idx  # 0 (óptimo) … 3 (malo)

        porcentaje = round((puntaje_total / maximo_total) * 100)

        return render_template(
            'resultados.html',
            respuestas=respuestas,
            segmentos=segmentos,
            porcentaje=porcentaje
        )

    return render_template('index.html', segmentos=segmentos)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
