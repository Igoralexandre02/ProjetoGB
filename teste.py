import pdfplumber
import pandas as pd
import re

# 1. Extração dos códigos do PDF
def extrair_codigos_pdf(caminho_pdf):
    codigos = set()
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
                 
            codigo = re.search(r"(?<=\d/2024)[A-Z0-9]+(?=/\d)", texto)
                
            if codigo:  # Adapte conforme o padrão real
                codigo = codigo.group().split()  # Supondo que o código está no início da linha
                codigos.add(codigo)
                
    return codigos

# 2. Leitura dos códigos da fatura
def ler_codigos_fatura(caminho_fatura):
    # Adapte conforme o formato da fatura (exemplo: CSV, Excel, etc.)
    df = pd.read_excel(caminho_fatura)  # Ou pd.read_csv() para CSV
    return set(df["codigo"])  # Supondo que a coluna dos códigos se chama 'codigo'

# 3. Comparação
def comparar_codigos(codigos_pdf, codigos_fatura):
    nao_pagamentos = codigos_pdf - codigos_fatura
    pagamentos_extras = codigos_fatura - codigos_pdf
    return nao_pagamentos, pagamentos_extras

# Caminhos dos arquivos
caminho_pdf = r"C:\Users\igora\OneDrive\Documents\Bilhetes\fatura_16.pdf"  # Insira o caminho correto
caminho_fatura = r"C:\Users\igora\OneDrive\Documents\Bilhetes\fatura_16.pdf"  # Insira o caminho correto

# Processamento
codigos_pdf = extrair_codigos_pdf(caminho_pdf)
codigos_fatura = ler_codigos_fatura(caminho_fatura)
nao_pagamentos, pagamentos_extras = comparar_codigos(codigos_pdf, codigos_fatura)

# Resultados
print("Bilhetes que não constam na fatura (não pagos):", nao_pagamentos)
print("Bilhetes que estão na fatura, mas não constam no PDF:", pagamentos_extras)