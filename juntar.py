import os
from PyPDF2 import PdfMerger

# Caminho do diretório principal
diretorio = r"C:\Users\igora\OneDrive\Documents\Bilhetes\0029.050651.2024-16 - VERIFICADO"

# Nome do arquivo PDF de saída
arquivo_saida = os.path.join(diretorio, "bilhetes_juntos.pdf")

# Cria um objeto PdfMerger
merger = PdfMerger()

# Loop através do diretório e suas subpastas
for pasta_raiz, pastas, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        if arquivo.endswith('.pdf'):
            caminho_pdf = os.path.join(pasta_raiz, arquivo)
            merger.append(caminho_pdf)

# Escreve o arquivo PDF combinado
merger.write(arquivo_saida)
merger.close()

print(f"Arquivos PDF unidos em: {arquivo_saida}")
