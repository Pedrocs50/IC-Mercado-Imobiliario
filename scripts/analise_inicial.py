import pandas as pd
import os

# 1. Carregar os dados
caminho_arquivo = 'data/raw/anuncios_jacarei_completo_v2.csv'

if not os.path.exists(caminho_arquivo):
    print("❌ Arquivo não encontrado! Rode o scraper primeiro.")
else:
    df = pd.read_csv(caminho_arquivo)

    print("--- 📊 RESUMO DOS DADOS COLETADOS ---")
    print(f"Total de imóveis: {len(df)}")
    print("\n--- 🔍 PRIMEIRAS LINHAS ---")
    print(df.head())

    print("\n--- ❓ VALORES FALTANTES (N/A) ---")
    print(df.isnull().sum())
    
    # Mostrar quantas linhas tem de 'N/A' que o Selenium marcou
    print("\n--- 🛠️ DADOS PARA LIMPAR (Marcados como N/A) ---")
    print((df == 'N/A').sum())