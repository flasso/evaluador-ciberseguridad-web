from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", [(3, "Dedicado y certificado"), (2, "Interno no exclusivo"), (1, "Proveedor externo"), (0, "Ninguno")]),
        ("¿Monitorean la seguridad regularmente?", [(3, "Diario/24x7"), (2, "Semanal"), (1, "Mensual"), (0, "No")]),
        ("¿Tienen inventario actualizado de equipos/datos?", [(3, "Sí, detallado"), (2, "Sí, incompleto"), (1, "Parcial"), (0, "No")]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", [(3, "Sí, gestionado"), (2, "Sí, mal configurado"), (1, "Solo software"), (0, "No firewall")]),
        ("¿Quién gestiona el firewall?", [(3, "Experto interno"), (2, "Proveedor MSSP"), (1, "TI no especializado"), (0, "No hay firewall")]),
        ("¿Wi-Fi está segura y separada para invitados?", [(3, "Sí, WPA3 y segmentada"), (2, "Sí, pero débil"), (1, "No segura"), (0, "No")]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR en todos los equipos?", [(3, "Sí, EDR"), (2, "Sí, antivirus básico"), (1, "Gratis"), (0, "No")]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", [(3, "Sí, con política definida y gestor"), (2, "Sí, pero inconsistente"), (1, "No realmente"), (0, "No")]),
        ("¿Actualizan el sistema operativo y software con parches recientes?", [(3, "Automatizado"), (2, "Manual"), (1, "Irregular"), (0, "No")]),
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", [(3, "Sí, en todas"), (2, "Sí, en algunas"), (1, "Pocas"), (0, "No")]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", [(3, "Sí, diario"), (2, "Semanal"), (1, "Mensual"), (0, "No")]),
        ("¿Prueban restauración de respaldos?", [(3, "Sí, programada"), (2, "Ocasional"), (1, "Nunca"), (0, "No sabe")]),
        ("¿Capacita regularmente a sus empleados en ciberseguridad?", [(3, "Al menos 1 vez/año"), (2, "Sí, pero informal"), (1, "Rara vez"), (0, "Nunca")]),
        ("¿Tiene responsable para las copias de seguridad?", [(3, "Personal especializado"), (2, "TI no especializado"), (1, "Nadie asignado"), (0, "No se hace")]),
    ])
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        respuestas = {k: int(v) for k, v in request.form.items()}
        total = sum(respuestas.values())
        max_total = len(respuestas) * 3
        porcentaje = round((total / max_total) * 100, 1)

        nivel = ""
        if porcentaje < 40:
            nivel = "🚨 Riesgo Crítico"
        elif porcentaje < 70:
            nivel = "🔶 Postura Básica"
        elif porcentaje < 90:
            nivel = "✅ Postura Sólida"
        else:
            nivel = "🏆 Postura Avanzada"

        return render_template('resultados.html', respuestas=respuestas, segmentos=segmentos,
                               porcentaje=porcentaje, nivel=nivel)

    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
