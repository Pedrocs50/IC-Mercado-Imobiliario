import time
import os
import random
import pandas as pd
import undetected_chromedriver as uc # <--- A ferramenta nova
from selenium.webdriver.common.by import By

# --- CONFIGURAÇÃO ---
# O uc.Chrome baixa o driver sozinho se precisar, mas vamos apontar para o seu
CHROME_BIN_PATH = os.path.join(os.getcwd(), 'scripts', 'chrome-win64', 'chrome.exe')

options = uc.ChromeOptions()
options.binary_location = CHROME_BIN_PATH
options.add_argument("--start-maximized")

print("🚀 Iniciando Navegador Indetectável...")

# O UC já faz a mágica de esconder que é automação aqui:
driver = uc.Chrome(options=options, version_main=145) 

url_base = "https://www.zapimoveis.com.br/venda/imoveis/sp+jacarei/"
total_paginas = 5
dados_imoveis = []

for p in range(1, total_paginas + 1):
    url_paginada = f"{url_base}?page={p}"
    print(f"\n--- 📄 Tentando Página {p} ---")
    
    driver.get(url_paginada)

    # O Cloudflare as vezes pede um desafio de "Verificar se você é humano"
    # Se ele aparecer, você resolve NO MOUSE e o código continua.
    time.sleep(random.uniform(15, 25)) 

    # --- BUSCANDO OS CARDS ---
    anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    if len(anuncios) == 0:
        print("⚠️ Bloqueio detectado ou página vazia.")
        input("Resolva o desafio na tela e aperte ENTER aqui...")
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    # --- EXTRAÇÃO (Igual ao que já funcionava) ---
    for anuncio in anuncios:
        try:
            preco = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
            endereco = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text
            
            dados_imoveis.append({
                'pagina': p,
                'endereco': endereco,
                'preco': preco.replace('\n', ' ').strip()
            })
        except: continue
    
    print(f"✅ Acumulado: {len(dados_imoveis)} imóveis.")

# --- SALVAMENTO ---
if dados_imoveis:
    df = pd.DataFrame(dados_imoveis)
    df.to_csv('data/raw/anuncios_jacarei_completo.csv', index=False, encoding='utf-8-sig')
    print(f"\n🏆 SUCESSO! Dados salvos.")

driver.quit()