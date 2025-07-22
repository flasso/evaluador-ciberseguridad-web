from flask import Flask, render_template, request

app = Flask(__name__)

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
        ("¿Tienen antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Sí, programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Sí, pero informal", "Rara vez", "Nunca"]),
        ("¿Tiene responsable para las copias de seguridad?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ])
]

pesos = {
    "¿Respaldan datos críticos a diario?": 2,
    "¿Prueban restauración de respaldos?": 2,
    "¿Tienen antivirus/EDR en todos los equipos?": 2,
    "¿Capacita regularmente a sus empleados en ciberseguridad?": 2,
}

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = {}
        puntos_obtenidos = 0
        puntos_maximos = 0

        for segmento, preguntas in segmentos:
            for pregunta, opciones in preguntas:
                idx_str = request.form.get(pregunta)
                idx = int(idx_str) if idx_str else 0
                respuesta_texto = opciones[idx]
                respuestas[pregunta] = respuesta_texto

                peso = pesos.get(pregunta, 1)
                puntos_obtenidos += idx * peso
                puntos_maximos += 3 * peso

        porcentaje = round((puntos_obtenidos / puntos_maximos) * 100, 1) if puntos_maximos else 0

        return render_template(
            'resultados.html',
            respuestas=respuestas,
            segmentos=segmentos,
            porcentaje=porcentaje
        )

    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
