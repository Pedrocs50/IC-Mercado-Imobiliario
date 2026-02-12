import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# -- CONFIGURAÇÃO --
CHROME_DRIVER_PATH = 'scripts/chromedriver.exe'
service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# -- EXECUÇÃO DA MISSÃO --
print("Iniciando a missão de reconhecimento no Zap Imóveis...")

# 1. DEFINIR A URL ALVO
url_zap = "https://www.zapimoveis.com.br/venda/imoveis/sp+jacarei/"

# 2. NAVEGAR ATÉ O ALVO
print(f"Navegando para: {url_zap}")
driver.get(url_zap)

# 3. AGUARDAR O CARREGAMENTO
# Damos um tempo generoso para o site carregar todo o JavaScript.
print("Aguardando o site carregar completamente (10 segundos)...")
time.sleep(10)

# 4. EXECUTAR A EXTRAÇÃO SIMPLES
# O Selenium nos dá acesso a várias informações da página.
# Vamos pegar o título que aparece na aba do navegador.
titulo_da_pagina = driver.title
print("-" * 30)
print(f"Missão bem-sucedida! O título da página é:")
print(f"'{titulo_da_pagina}'")
print("-" * 30)


# 5. FINALIZAR A MISSÃO
print("Reconhecimento concluído. Fechando o navegador.")
driver.quit()