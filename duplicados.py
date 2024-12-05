import os
import re
from PyPDF2 import PdfReader
import shutil

# Diretório onde estão os arquivos PDF
directory = r'C:\Users\05107553214\Documents\Bilhetes\0029.050651.2024-16 - VERIFICADO\VALE-DO-ANARI - VERIFICADO'

# Criar pasta para bilhetes duplicados, se não existir
duplicate_folder = os.path.join(directory, "BILHETES DUPLICADOS")
os.makedirs(duplicate_folder, exist_ok=True)

# Dicionário para armazenar os dados dos bilhetes
tickets = {}

# Função para extrair informações do PDF
def extract_info(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Captura o nome da transportadora
    transportadora = re.search(r'(SOLIMOES)', text) # Procura no documento o nome "SOLIMOES"
    transportadora = re.search(r'(AMATUR)', text)
    transportadora = transportadora.group(1) if transportadora else 'SERRA AZUL' # Caso não encontrado o primeiro nome "SOLIMOES", então "AMATUR" é a trasportadora
                   
    if transportadora == 'AMATUR':
        origem = re.search(r'Deficiência:\n\s*([A-ZÀ-ÿ\s-]+)(?=\s*-\s)', text) 
        destino = re.search(r'Origem:\n\s*([^\n-]+)', text) 
        data = re.search(r'Destino:\n([^\|]+)(?=\s*Data:)', text) 
        horario = re.search(r'Horário:([^\(\n]+)', text) 
        texto_limpo = re.sub(r'[^A-Za-zÀ-ÿ\s\n]', '', text)
        passageiro = re.search(r'Outros\s+\n\s*([A-ZÀ-ÿ\s]+)(?=\n)', texto_limpo)
    else :
        # Captura origem e destino
        origem = re.search(r'Origem:\s*([^\(]+)', text) 
        destino = re.search(r'Destino:\s*([^\(]+)', text) 
        data = re.search(r'Data:\s*([^\|]+)', text) 
        horario = re.search(r'Horário:\s*([^\(\n]+)', text) 
        passageiro = re.search(r'Passageiro:\s*DOC:\s*\d+\s*-\s*(.*)', text) 
    
    origem = origem.group(1).strip().replace("\n", " ") if origem else "Origem not found"
    destino = destino.group(1).strip().replace("\n", " ") if destino else "Destino not found"
    data = data.group(1).strip() if data else "Data not found"
    horario = horario.group(1).strip() if horario else "Horario not found"
    passageiro = passageiro.group(1).strip().replace("\n", " ") if passageiro else "Nome not found"
    
    return (passageiro, origem, destino, data, horario)

# Percorrer todos os arquivos no diretório
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        file_path = os.path.join(directory, filename)
        ticket_info = extract_info(file_path)

        if ticket_info in tickets:
            # Mover arquivo para a pasta de duplicados
            shutil.move(file_path, os.path.join(duplicate_folder, filename))
            print(f'Movido: {filename} para BILHETES DUPLICADOS')
        else:
            # Adicionar informações ao dicionário
            tickets[ticket_info] = filename

print("Processo concluído!")
