import time
import os
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- CONFIGURAÇÃO ---
CHROME_BIN_PATH = os.path.join(os.getcwd(), 'scripts', 'chrome-win64', 'chrome.exe')

options = uc.ChromeOptions()
options.binary_location = CHROME_BIN_PATH
options.add_argument("--start-maximized")

print("Iniciando Navegador para Extração Completa...")

# Inicializa o driver (o version_main deve bater com a versão do seu chrome de teste)
driver = uc.Chrome(options=options, version_main=145) 

url_base = "https://www.zapimoveis.com.br/venda/imoveis/sp+jacarei/"
total_paginas = 25
dados_imoveis = []

for p in range(1, total_paginas + 1):
    url_paginada = f"{url_base}?page={p}"
    print(f"\n--- 📄 Acessando Página {p} de {total_paginas} ---")
    
    driver.get(url_paginada)

    # Tempo variável para simular comportamento humano
    tempo_random = random.uniform(15, 25)
    print(f"Aguardando {tempo_random:.2f}s...")
    time.sleep(tempo_random)

    # Simula uma rolagem leve para carregar elementos
    driver.execute_script("window.scrollTo(0, 500);")

    # --- BUSCANDO OS CARDS ---
    anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    if len(anuncios) == 0:
        print("⚠️ Bloqueio ou página vazia detectada.")
        input("Resolva o desafio na tela e aperte ENTER aqui no terminal...")
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[class*="content-stretch"][class*="min-w-0"]')

    print(f"Encontrados {len(anuncios)} anúncios.")

    # --- EXTRAÇÃO DETALHADA ---
    for anuncio in anuncios:
        try:
            # 1. Preço (Obrigatório para validar o card)
            try:
                preco_raw = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
                preco_limpo = preco_raw.replace('\n', ' ').strip()
            except:
                continue

            # 2. Endereço / Localização
            try:
                endereco = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text
            except:
                endereco = "N/A"

            # 3. Área (m²)
            try:
                area = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text
            except:
                area = "N/A"

            # 4. Quartos
            try:
                quartos = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text
            except:
                quartos = "N/A"

            # 5. Banheiros
            try:
                banheiros = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]').text
            except:
                banheiros = "N/A"

            # 6. Vagas de Garagem
            try:
                vagas = anuncio.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').text
            except:
                vagas = "N/A"

            # salvando as informações extraidas em uma tabela
            dados_imoveis.append({
                'pagina': p,
                'endereco': endereco,
                'preco': preco_limpo,
                'area': area,
                'quartos': quartos,
                'banheiros': banheiros,
                'vagas': vagas
            })
            
        except Exception:
            continue
    
    print(f"✅ Total acumulado: {len(dados_imoveis)} imóveis.")

# --- SALVAMENTO ---
if dados_imoveis:
    df = pd.DataFrame(dados_imoveis)
    os.makedirs('data/raw', exist_ok=True)
    
    # Salvando com todas as colunas
    arquivo_final = 'data/raw/anuncios_jacarei_completo_v2.csv'
    df.to_csv(arquivo_final, index=False, encoding='utf-8-sig')
    print(f"\n🏆 SUCESSO! Tabela completa com {len(df)} linhas salva em: {arquivo_final}")
else:
    print("\n❌ Nenhum dado foi coletado.")

driver.quit()