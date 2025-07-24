import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! Actualiza esto con la ruta REAL a tu ejecutable de WebDriver.
# Ejemplo para Windows: 'C:\\ruta\\a\\tu\\chromedriver.exe'
# Ejemplo para Linux/macOS (si no está en PATH): '/usr/local/bin/chromedriver'
WEBDRIVER_PATH = 'C:\\ruta\\a\\tu\\chromedriver.exe' # <--- ¡CAMBIA ESTO!

# Nombre del archivo con los datos de los perros
ARCHIVO_DATOS_PERROS = "perros.txt"

# --- FUNCIONES ---

def leer_datos_perros(nombre_archivo):
    """Lee los datos de los perros desde un archivo de texto separado por punto y coma."""
    datos_perros = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(';')
                if len(partes) == 4:
                    datos_perros.append({
                        "nombre": partes[0],
                        "saludo": partes[1],
                        "pregunta": partes[2],
                        "sugerencia": partes[3]
                    })
                else:
                    print(f"Advertencia: Línea mal formada en {nombre_archivo}: {linea.strip()}")
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
    return datos_perros

def enviar_mensaje_whatsapp(nombre_contacto, texto_mensaje):
    """
    Envía un mensaje de WhatsApp a un contacto específico usando Selenium.
    Requiere escaneo manual del código QR la primera vez o si la sesión expira.
    """
    service = Service(WEBDRIVER_PATH)
    options = webdriver.ChromeOptions()
    # Esta opción ayuda a mantener la sesión de WhatsApp Web iniciada
    # para no tener que escanear el QR cada vez.
    options.add_argument("user-data-dir=./perfil_selenium") # Se creará en la misma carpeta del script

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")

    print(f"Intentando enviar mensaje a '{nombre_contacto}'. Asegúrate de que WhatsApp Web esté iniciado.")
    print("Esperando hasta 60 segundos para que cargue WhatsApp Web...")

    # Espera explícita para que cargue la página y el usuario escanee el QR si es necesario
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]')) # Un elemento que indica que WhatsApp Web cargó
        )
        print("WhatsApp Web cargado.")
    except Exception:
        print("Error: WhatsApp Web no cargó en el tiempo esperado. Asegúrate de tener conexión y haber escaneado el QR.")
        driver.quit()
        return

    try:
        # 1. Buscar el contacto
        # INSPECCIONA WHATSAPP WEB PARA ENCONTRAR EL SELECTOR CORRECTO DEL CUADRO DE BÚSQUEDA.
        # Los XPATHs pueden cambiar con las actualizaciones de WhatsApp Web.
        # Podría ser un input con un 'data-testid' o 'aria-label'.
        # Ejemplo: search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        # O busca por data-testid="search-input" o similar.
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]'))
            # Este XPath es un ejemplo común, pero puede variar.
            # Busca algo como '//div[@data-testid="search"]//input' o similar.
        )
        search_box.send_keys(nombre_contacto)
        time.sleep(5) # Espera a que aparezcan los resultados de búsqueda

        # 2. Hacer clic en el contacto
        # Esto también depende mucho de cómo se muestren los resultados de búsqueda.
        # Generalmente, es un span con el nombre del contacto.
        try:
            contacto_elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@title='{nombre_contacto}']"))
            )
            contacto_elemento.click()
            time.sleep(5) # Espera a que se abra el chat
        except Exception as e:
            print(f"No se pudo encontrar el contacto '{nombre_contacto}' en los resultados de búsqueda. Error: {e}")
            return # Salir si no se encuentra el contacto

        # 3. Escribir y enviar el mensaje
        # INSPECCIONA WHATSAPP WEB PARA ENCONTRAR EL SELECTOR CORRECTO DEL CUADRO DE MENSAJE.
        # Busca el input o div contenteditable donde escribes los mensajes.
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]'))
            # Otro XPath común que puede cambiar. Busca un div con 'contenteditable="true"' o un 'data-testid="compose-box"'
        )
        message_box.send_keys(texto_mensaje)
        message_box.send_keys(Keys.ENTER) # Envía el mensaje
        time.sleep(3) # Da tiempo para que se envíe el mensaje
        print(f"Mensaje enviado exitosamente a {nombre_contacto}.")

    except Exception as e:
        print(f"Ocurrió un error al enviar el mensaje a {nombre_contacto}: {e}")
    finally:
        driver.quit() # Cierra el navegador al finalizar

# --- LÓGICA PRINCIPAL DEL PROGRAMA ---
if __name__ == "__main__":
    perros_a_mensajear = leer_datos_perros(ARCHIVO_DATOS_PERROS)

    if not perros_a_mensajear:
        print("No se encontraron datos de perros o el archivo está vacío. Saliendo.")
    else:
        for perro in perros_a_mensajear:
            # Construye el mensaje completo
            mensaje_completo = (
                f"{perro['saludo']} {perro['nombre']}! {perro['pregunta']} "
                f"¡{perro['sugerencia']}"
            )
            print(f"\nPreparando para enviar mensaje a {perro['nombre']}: {mensaje_completo}")
            # El nombre del contacto de WhatsApp debe coincidir exactamente con perro['nombre']
            send_whatsapp_message(perro['nombre'], mensaje_completo)
            time.sleep(15) # Espera un poco entre mensajes para evitar bloqueos
        print("\nFinalizado el intento de enviar todos los mensajes.")