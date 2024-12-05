import PyPDF2
import re
from collections import Counter

# Função para ler um PDF e extrair números de bilhetes
def pdf_para_bilhetes(pdf_path, txt_path):
    bilhetes = []

    # Abrindo o arquivo PDF
    with open(pdf_path, 'rb') as pdf_file:
        # Criando um objeto PDF Reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Iterando pelas páginas do PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto = page.extract_text()
            
            # Verifica se o texto não é None
            if texto:
                # Usando uma expressão regular para encontrar os números dos bilhetes
                # O padrão busca por sequências que parecem números de bilhetes (ex: C221B, 767C9)
                numeros_encontrados = re.findall(r'/\d{4}\n([A-Z0-9]+) \n\d{2}/', texto)
                
                # Adicionando os números encontrados à lista
                bilhetes.extend(numeros_encontrados)

    # Contando a ocorrência de cada número de bilhete
    contagem_bilhetes = Counter(bilhetes)

    # Salvando a contagem em um arquivo texto
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for bilhete, contagem in contagem_bilhetes.items():
            txt_file.write(f"{bilhete}: {contagem}\n")

# Exemplo de uso
pdf_path = r'C:\Users\05107553214\Documents\Bilhetes\Fatura\Fatura.pdf'
txt_path = r'C:\Users\05107553214\Documents\Bilhetes\Fatura\Fatura_texto.txt'
pdf_para_bilhetes(pdf_path, txt_path)

print("Extração e salvamento de bilhetes concluídos!")
