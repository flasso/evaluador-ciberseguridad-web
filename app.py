from flask import Flask, render_template, request

app = Flask(__name__)

segmentos = [
    ("Gestión y Visibilidad", [
        ("¿Quién es el responsable de TI/ciberseguridad?", ["Dedicado y certificado", "Interno no exclusivo", "Proveedor externo", "Ninguno"]),
        ("¿Monitorean regularmente el estado de los equipos?", ["Sí, diariamente", "Sí, semanalmente", "Sí, ocasionalmente", "No"]),
        ("¿Tienen inventario actualizado de equipos/datos?", ["Sí, detallado", "Sí, incompleto", "Parcial", "No"]),
        ("¿Tienen un plan de respuesta definido para ataques (ej. virus, ransomware)?", ["Sí, documentado y probado", "Sí, documentado pero no probado", "Solo una idea básica", "No"]),
        ("¿Realizan monitoreo regular de la postura de ciberseguridad?", ["Sí, trimestral", "Sí, anual", "Irregular", "No"]),
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
        ("¿Tienen MFA (Autenticación Multifactor) activada en cuentas críticas?", ["Sí, en todas", "Sí, en algunas", "Pocas", "No"]),
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

        puntaje = 0
        max_puntaje = len(respuestas) * 3
        for r in respuestas.values():
            if r == "Dedicado y certificado" or r == "Sí, diariamente" or r == "Sí, detallado" or r == "Sí, documentado y probado" or r == "Sí, trimestral" or r == "Sí, gestionado" or r == "Sí, WPA3 y segmentada" or r == "Sí, EDR" or r == "Sí, con política definida y gestor" or r == "Automatizado" or r == "Sí, en todas" or r == "Herramientas seguras (ej. RMM)" or r == "Sí, diario" or r == "Sí, programada" or r == "Al menos 1 vez/año" or r == "Personal especializado":
                puntaje += 3
            elif r in ["Interno no exclusivo", "Sí, semanalmente", "Sí, incompleto", "Sí, documentado pero no probado", "Sí, anual", "Sí, mal configurado", "Sí, pero débil", "Sí, antivirus básico", "Sí, pero inconsistente", "Manual", "Sí, en algunas", "TeamViewer/AnyDesk con control", "Semanal", "Ocasional", "Sí, pero informal", "TI no especializado"]:
                puntaje += 2
            elif r in ["Proveedor externo", "Sí, ocasionalmente", "Parcial", "Solo una idea básica", "Irregular", "Solo software", "No segura", "Gratis", "No realmente", "Irregular", "Pocas", "Acceso remoto sin control", "Mensual", "Nunca", "Rara vez", "Nadie asignado"]:
                puntaje += 1

        porcentaje = round(puntaje / max_puntaje * 100)

        return render_template('resultados.html', respuestas=respuestas, segmentos=segmentos, encabezado=encabezado, porcentaje=porcentaje)
    return render_template('index.html', segmentos=segmentos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
