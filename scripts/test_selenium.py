import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# -- CONFIGURAÇÃO --
# O caminho para o chromedriver.exe que você colocou na pasta /scripts
# Como o script e o chromedriver estão na mesma pasta, só o nome do arquivo basta.
CHROME_DRIVER_PATH = 'scripts/chromedriver.exe' 

# Cria um objeto de serviço, apontando para o nosso chromedriver
service = Service(executable_path=CHROME_DRIVER_PATH)

# Cria a instância do navegador Chrome, usando o serviço
driver = webdriver.Chrome(service=service)

# -- EXECUÇÃO DO TESTE --
print("Iniciando o voo de teste...")

# 1. Abrir o navegador e navegar para uma página
print("Navegando para o Google...")
driver.get("https://www.google.com")

# 2. Esperar um pouco para a gente conseguir ver a mágica
print("Aguardando 5 segundos...")
time.sleep(5)

# 3. Fechar o navegador
print("Teste concluído. Fechando o navegador.")
driver.quit()