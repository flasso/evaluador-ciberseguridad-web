from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean regularmente el estado de los equipos?", ["Sí, diariamente", "Sí, semanalmente", "Sí, ocasionalmente", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Tienen un plan de respuesta definido para ataques (ej. ransomware)?", ["Sí, documentado y probado", "Sí, documentado pero no probado", "Solo una idea básica", "No"]),
    ]),
    ("Protección de Red", [
        ("¿Tienen firewall de hardware o UTM?", ["Sí, gestionado", "Sí, mal configurado", "Solo software", "No"]),
        ("¿Quién gestiona el firewall?", ["Experto interno", "Proveedor MSSP", "TI no especializado", "No hay firewall"]),
        ("¿Wi-Fi está segura y separada para invitados?", ["Sí, WPA3 y segmentada", "Sí, pero débil", "No segura", "No"]),
    ]),
    ("Protección de Dispositivos", [
        ("¿Tienen antivirus con EDR en todos los equipos?", ["Sí, EDR", "Sí, antivirus básico", "Gratis", "No"]),
        ("¿Las contraseñas son seguras y se actualizan periódicamente?", ["Sí, con política definida y gestor", "Sí, pero inconsistente", "No realmente", "No"]),
        ("¿Actualizan sistema operativo y software con parches recientes?", ["Automatizado", "Manual", "Irregular", "No"]),
        ("¿Tienen MMFA (Autenticación Multifactor)FA activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
        ("¿Cómo gestionan remotamente los equipos?", ["Herramientas seguras (ej. RMM)", "TeamViewer/AnyDesk con control", "Acceso remoto sin control", "No gestionan"]),
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
        respuestas = request.form.to_dict()
        encabezado = {
            "empresa": respuestas.pop("empresa", ""),
            "contacto": respuestas.pop("contacto", ""),
            "email": respuestas.pop("email", ""),
            "sector": respuestas.pop("sector", ""),
            "pcs": respuestas.pop("pcs", "")
        }
        return render_template('resultados.html', respuestas=respuestas, segmentos=segmentos, encabezado=encabezado)
    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
