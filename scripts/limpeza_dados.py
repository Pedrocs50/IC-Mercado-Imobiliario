import pandas as pd
import re
import os

# --- CONFIGURAÇÃO DE CAMINHOS ---
ARQUIVO_RAW = 'data/raw/anuncios_jacarei_completo_v2.csv'
PASTA_PROCESSADOS = 'data/processed'
os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

def extrair_numero(texto):
    if pd.isna(texto) or texto == 'N/A': 
        return None
    # Pega apenas os dígitos, ignorando pontos, quebras de linha e textos
    numeros = re.findall(r'\d+', str(texto).replace('.', ''))
    return float(numeros[0]) if numeros else None

def definir_tipo(titulo):
    titulo = str(titulo).lower()
    if 'apartamento' in titulo:
        return 'Apartamento'
    elif 'casa' in titulo or 'sobrado' in titulo:
        return 'Casa'
    elif 'terreno' in titulo or 'lote' in titulo:
        return 'Terreno'
    return 'Outro'

def limpar_preco(texto):
    if pd.isna(texto): return None
    # Pega o valor principal antes de menções a Condomínio ou IPTU
    limpo = str(texto).split('Cond')[0].split('IPTU')[0]
    valor = re.sub(r'[^\d]', '', limpo)
    return float(valor) if valor else None

# --- EXECUÇÃO DA LIMPEZA ---
df = pd.read_csv(ARQUIVO_RAW)

# 1. Categorizar o imóvel
df['tipo'] = df['endereco'].apply(definir_tipo)

# 2. Limpar números (Área, Quartos, Banheiros, Vagas)
df['area_m2'] = df['area'].apply(extrair_numero)
df['preco_venda'] = df['preco'].apply(limpar_preco)
df['qtd_quartos'] = df['quartos'].apply(extrair_numero)
df['qtd_vagas'] = df['vagas'].apply(extrair_numero)

# 3. Criar métrica de preço/m2
df['preco_m2'] = df['preco_venda'] / df['area_m2']

# 4. Filtrar o "lixo" (Imóveis sem preço ou sem área não servem para IC)
df_clean = df.dropna(subset=['preco_venda', 'area_m2']).copy()

# 5. Separar os arquivos para facilitar a sua análise
df_residencial = df_clean[df_clean['tipo'].isin(['Casa', 'Apartamento'])]
df_terrenos = df_clean[df_clean['tipo'] == 'Terreno']

# --- SALVAMENTO ---
df_residencial.to_csv(f'{PASTA_PROCESSADOS}/imoveis_residenciais.csv', index=False, encoding='utf-8-sig')
df_terrenos.to_csv(f'{PASTA_PROCESSADOS}/terrenos_jacarei.csv', index=False, encoding='utf-8-sig')

print(f"✅ Limpeza Concluída!")
print(f"🏠 Residencial (Casas/Aptos): {len(df_residencial)} imóveis")
print(f"🌳 Terrenos: {len(df_terrenos)} lotes")