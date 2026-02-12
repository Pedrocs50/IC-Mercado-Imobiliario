import time
import os
import random  # NOVO: Para gerar tempos aleatórios
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- CONFIGURAÇÃO ---
caminho_base = os.getcwd()
DRIVER_PATH = os.path.join(caminho_base, 'scripts', 'chromedriver.exe')
CHROME_BIN_PATH = os.path.join(caminho_base, 'scripts', 'chrome-win64', 'chrome.exe')

chrome_options = Options()
chrome_options.binary_location = CHROME_BIN_PATH

# --- DISFARCES (USER-AGENT E FLAGS) ---
# 1. Faz o Chrome parecer um navegador real de uso diário
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 2. Desativa a mensagem "O Chrome está sendo controlado por software de teste"
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# 3. Outros disfarces técnicos
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")

service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- CONFIGURAÇÃO DA MISSÃO ---
url_base = "https://www.zapimoveis.com.br/venda/imoveis/sp+jacarei/"
total_paginas = 5 
dados_imoveis = []

print(f"🚀 Iniciando extração camuflada de {total_paginas} páginas...")

for p in range(1, total_paginas + 1):
    url_paginada = f"{url_base}?page={p}"
    print(f"\n--- 📄 Acessando Página {p} ---")
    
    driver.get(url_paginada)

    # 4. TEMPO ALEATÓRIO: Entre 12 e 20 segundos
    tempo_espera = random.uniform(12, 20)
    print(f"Aguardando {tempo_espera:.2f} segundos (tempo variável)...")
    time.sleep(tempo_espera)

    # 5. SIMULAR ROLAGEM: Rola um pouco para baixo para parecer humano
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)

    # --- ENCONTRANDO OS CARDS ---
    anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    if len(anuncios) == 0:
        print("⚠️ Atenção: 0 anúncios. Pode ser um CAPTCHA ou bloqueio.")
        # Se você ver o desafio na tela, resolva manualmente e o robô continua
        input("Resolva o desafio no navegador (se houver) e aperte ENTER para continuar...")
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    print(f"Encontrados {len(anuncios)} anúncios.")

    # --- EXTRAÇÃO DOS DADOS ---
    for anuncio in anuncios:
        try:
            try:
                preco_texto = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
            except:
                continue

            try: endereco = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text
            except: endereco = "N/A"

            try: area = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text
            except: area = "N/A"

            try: quartos = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text
            except: quartos = "N/A"

            dados_imoveis.append({
                'pagina': p,
                'endereco': endereco,
                'preco': preco_texto.replace('\n', ' ').strip(),
                'area': area,
                'quartos': quartos
            })
        except:
            continue
    
    print(f"✅ Página {p} concluída. Total acumulado: {len(dados_imoveis)}")

# --- SALVAMENTO ---
if dados_imoveis:
    df = pd.DataFrame(dados_imoveis)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/anuncios_jacarei_completo.csv', index=False, encoding='utf-8-sig')
    print(f"\n🏆 SUCESSO! {len(df)} imóveis salvos.")

driver.quit()