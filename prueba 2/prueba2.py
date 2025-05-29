import re
import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

usuario = "vafaret392@daxiake.com"
clave = "Colombia2025*"
limite = 10

# Cuentas objetivo
cuentas = ["elcorteingles", "mercadona", "carrefoures"]

# Crear Excel
wb = openpyxl.Workbook()
hoja = wb.active
hoja.title = "Seguidores"
hoja.append(["Cuenta", "Usuario", "Bio", "Correo", "Teléfono", "Fecha de unión"])

driver = webdriver.Chrome()
driver.get("https://www.instagram.com")
time.sleep(2)

# Iniciar sesión
driver.find_element(By.NAME, "username").send_keys(usuario)
driver.find_element(By.NAME, "password").send_keys(clave + Keys.RETURN)
time.sleep(5)

# Clic en "Ahora no"
try:
    ahora_no = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Ahora no']"))
    )
    ahora_no.click()
    
except:
    pass

for cuenta in cuentas:
    print(f"\n### Procesando cuenta @{cuenta} ###")

    # Ir al perfil
    driver.get(f"https://www.instagram.com/{cuenta}/")
    time.sleep(2)

    # Clic en seguidores
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "seguidores"))
    ).click()
    time.sleep(2)

    # Capturar seguidores
    seguidores = set()
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[2]"))
    )

    while len(seguidores) < limite:
        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        for link in links:
            user = link.text.strip()
            if user and user not in seguidores:
                seguidores.add(user)
                if len(seguidores) >= limite:
                    break
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(1)

    # Cerrar modal
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']//button"))
        ).click()
        time.sleep(2)
    except:
        pass

    # Visitar perfiles seguidores
    for seguidor in seguidores:
        print(f"\n Visitando perfil @{seguidor}")
        driver.get(f"https://www.instagram.com/{seguidor}/")
        time.sleep(1)

        correo = telefono = fecha_union = "No disponible"
        bio_texto = ""

        # Extraer bio
        try:
            bio = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_aa_c')]"))
            ).text
            bio_texto = bio
            print(f"Bio: {bio}")

            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", bio)
            if email_match:
                correo = email_match.group()

            phone_match = re.search(r"\+?\d[\d\s\-\(\)]{7,}", bio)
            if phone_match:
                telefono = phone_match.group()
        except:
            print("No se pudo extraer la bio")

        # Abrir opciones > Información sobre esta cuenta
        try:
            opciones_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Opciones']"))
            )
            opciones_btn.click()
            time.sleep(0.1)

            info_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Información sobre esta cuenta']"))
            )
            info_btn.click()
            time.sleep(0.1)

            fecha_elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, "//span[text()='Fecha en que se unió']/following-sibling::span"
                ))
            )
            fecha_union = fecha_elemento.text.strip()
        except:
            print("No se pudo extraer la fecha de unión")

        print(f"Fecha unión: {fecha_union}")
        print(f"Correo: {correo}")
        print(f"Teléfono: {telefono}")

        # Guardar en Excel con la cuenta de origen
        hoja.append([cuenta, seguidor, bio_texto, correo, telefono, fecha_union])

# Guardar archivo
wb.save("seguidores_info.xlsx")
print("\n Datos guardados en 'seguidores_info.xlsx'")

driver.quit()
