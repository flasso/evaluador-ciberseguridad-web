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
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus/EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, política definida", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan el sistema y software con los últimos parches?", ["Automatizado", "Manual regular", "Irregular", "No"]),
        ("¿Tienen MFA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
    ]),
    ("Respaldo y Conciencia", [
        ("¿Respaldan datos críticos a diario?", ["Sí, diario", "Semanal", "Mensual", "No"]),
        ("¿Prueban restauración de respaldos?", ["Programada", "Ocasional", "Nunca", "No sabe"]),
        ("¿Capacitan regularmente a sus empleados en ciberseguridad?", ["Al menos 1 vez/año", "Informal", "Rara vez", "Nunca"]),
        ("¿Quién es responsable de los respaldos?", ["Personal especializado", "TI no especializado", "Nadie asignado", "No se hace"]),
    ]),
]

puntajes = {
    "Dedicado y certificado": 3,
    "Interno no exclusivo": 2,
    "Proveedor externo": 1,
    "Ninguno": 0,
    "Diario/24x7": 3,
    "Semanal": 2,
    "Mensual": 1,
    "No": 0,
    "Sí, detallado": 3,
    "Sí, incompleto": 2,
    "Parcial": 1,
    "Sí, gestionado": 3,
    "Sí, mal configurado": 2,
    "Solo software": 1,
    "No firewall": 0,
    "Experto interno": 3,
    "Proveedor MSSP": 2,
    "TI no especializado": 1,
    "No hay firewall": 0,
    "Sí, WPA3": 3,
    "Sí, pero débil": 2,
    "No segura": 1,
    "Sí, EDR": 3,
    "Sí, antivirus básico": 2,
    "Gratis": 1,
    "Automatizado": 3,
    "Manual regular": 2,
    "Irregular": 1,
    "Sí, en todas": 3,
    "Sí, en algunas": 2,
    "Pocas": 1,
    "Al menos 1 vez/año": 3,
    "Informal": 2,
    "Rara vez": 1,
    "Nunca": 0,
    "Programada": 3,
    "Ocasional": 2,
    "Nunca": 1,
    "No sabe": 0,
    "Personal especializado": 3,
    "TI no especializado": 2,
    "Nadie asignado": 1,
    "No se hace": 0,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        respuestas = dict(request.form)
        puntos = sum(puntajes.get(r, 0) for r in respuestas.values())
        max_puntos = len(respuestas) * 3
        porcentaje = int((puntos / max_puntos) * 100) if max_puntos > 0 else 0
        return render_template('resultados.html', respuestas=respuestas, porcentaje=porcentaje)
    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)