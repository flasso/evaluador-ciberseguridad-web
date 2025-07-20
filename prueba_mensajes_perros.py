# --- CONFIGURACIÓN ---
# Nombre del archivo con los datos de los perros
ARCHIVO_DATOS_PERROS = "perros.txt"

# --- FUNCIONES ---

def leer_datos_perros(nombre_archivo):
    """
    Lee los datos de los perros desde un archivo de texto
    separado por punto y coma.
    """
    datos_perros = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                # Limpia espacios en blanco y divide la línea por el punto y coma
                partes = linea.strip().split(';')
                # Asegúrate de que haya exactamente 4 partes
                if len(partes) == 4:
                    datos_perros.append({
                        "nombre": partes[0],
                        "saludo": partes[1],
                        "pregunta": partes[2],
                        "sugerencia": partes[3]
                    })
                else:
                    # Imprime una advertencia si una línea no tiene el formato esperado
                    print(f"Advertencia: Línea mal formada en {nombre_archivo}: '{linea.strip()}' - Se esperaba 4 campos separados por ';' pero se encontraron {len(partes)}.")
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado. Asegúrate de que esté en la misma carpeta que el script.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    return datos_perros

# --- LÓGICA PRINCIPAL DEL PROGRAMA (Solo para prueba sin WhatsApp) ---
if __name__ == "__main__":
    print(f"Iniciando prueba de lectura del archivo '{ARCHIVO_DATOS_PERROS}'...")

    # Llama a la función para leer los datos
    perros_a_mensajear = leer_datos_perros(ARCHIVO_DATOS_PERROS)

    if not perros_a_mensajear:
        print("No se encontraron datos de perros o el archivo está vacío. No hay mensajes que generar.")
    else:
        print("\n--- Mensajes Generados (Simulación sin WhatsApp) ---")
        for i, perro in enumerate(perros_a_mensajear):
            # Construye el mensaje completo usando los datos del perro
            mensaje_completo = (
                f"{perro['saludo']} {perro['nombre']}! {perro['pregunta']} "
                f"¡{perro['sugerencia']}"
            )
            # Imprime el mensaje en la consola
            print(f"Mensaje {i+1} para {perro['nombre']}:")
            print(f"  '{mensaje_completo}'")
            print("-" * 30) # Separador para mejor lectura

        print("\nPrueba de generación de mensajes finalizada. Todo se mostró en la consola.")