from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv, os
from datetime import date
from datetime import datetime

options = Options()
options.add_argument("--headless")         
options.add_argument("--width=1920")        # larghezza finestra
options.add_argument("--height=1080")       # altezza finestra
driver = webdriver.Firefox(options=options)

oggi = date.today()
import os
link = "https://www.google.it/maps/place/McDonald's+Dossobuono/@45.389607,10.9007287,17z/data=!4m6!3m5!1s0x4781e089d18461af:0x1eed8b83b934aa4c!8m2!3d45.389607!4d10.9033036!16s%2Fg%2F11cs39j4gr?entry=ttu&g_ep=EgoyMDI1MDQzMC4xIKXMDSoASAFQAw%3D%3D"
driver.get(link)
write_header = not os.path.exists("Dossobuono.csv") or os.path.getsize("Dossobuono.csv") == 0
try:
    # Accetta i cookie, se il pulsante è presente
    bottone_accetta = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Accetta tutto"]]'))
    )
    bottone_accetta.click()
except Exception:
    pass  # Se il pulsante non appare, continua
try:
  
    #Estrazione del testo di affollamento
    affollamento_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.UgBNB.fontBodySmall"))
    )

    # Scroll fino all'elemento
    driver.execute_script("arguments[0].scrollIntoView(true);", affollamento_element)

    # Leggi il testo dinamico
    affollamento_text = affollamento_element.text
    print("Affollamento:", affollamento_text)

    Tot_affluenza = driver.find_elements(By.CLASS_NAME, "dpoVLd")
   # with lock:
    with open(f'Dossobuono.csv', 'a', newline='', encoding='utf-8') as csvfile:
          fieldnames = ['Affluenza', 'Locale', 'Recensioni', 'Via','Link','Oggi','RealTime']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
          if write_header:
            writer.writeheader()  # scrive l'header solo se il file non esiste o è vuoto
          for affluenza in Tot_affluenza:
              estrattore = affluenza.get_attribute("aria-label")
              out = driver.find_element(By.CLASS_NAME, "DUwDvf").text
              recensione = driver.find_element(By.CLASS_NAME, "F7nice").text.replace("\n", " ")
              via = driver.find_element(By.CLASS_NAME, "Io6YTe").text
              writer.writerow({'Affluenza': estrattore, 'Locale': out, 'Recensioni': recensione, 'Via': via,'Link':link,'Oggi': oggi,'RealTime':affollamento_text})
              csvfile.flush()
                  #print(estrattore, out, recensione)  # Debug

except Exception as e:
    print(f"Errore durante l'elaborazione di {link}: {e}")
