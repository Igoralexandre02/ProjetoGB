import re
import os
import sqlite3
from PyPDF2 import PdfReader

# Conexão com o banco
conn = sqlite3.connect(r'C:\Users\igora\OneDrive\Documents\Dados\GB.db')
cursor = conn.cursor()

# Diretório onde estão os arquivos PDF
directory = r'C:\Users\igora\OneDrive\Documents\Bilhetes\0029.050651.2024-16 - VERIFICADO\VALE-DO-ANARI - VERIFICADO'

def extract_info(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Captura o nome da transportadora
    transportadora = re.search(r'(SOLIMOES)', text) 
    transportadora = re.search(r'(AMATUR)', text)
    transportadora = transportadora.group(1) if transportadora else 'SERRA AZUL' 

    # Captura as informações do bilhete
    if transportadora == 'AMATUR':
        origem = re.search(r'Deficiência:\n\s*([A-ZÀ-ÿ\s-]+)(?=\s*-\s)', text) 
        destino = re.search(r'Origem:\n\s*([^\n-]+)', text) 
        data = re.search(r'Destino:\n([^\|]+)(?=\s*Data:)', text) 
        horario = re.search(r'Horário:([^\(\n]+)', text) 
        texto_limpo = re.sub(r'[^A-Za-zÀ-ÿ\s\n]', '', text)
        passageiro = re.search(r'Outros\s+\n\s*([A-ZÀ-ÿ\s]+)(?=\n)', texto_limpo)
    else :
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
    
    return (passageiro, origem, destino, data, horario, transportadora)

# Percorrer todos os arquivos no diretório
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        file_path = os.path.join(directory, filename)
        pessoa, origem, destino, data, hora, transportadora = extract_info(file_path)
        
        # Inserir o nome na tabela Pessoa
        cursor.execute("INSERT OR IGNORE INTO Pessoa (Nome) VALUES (?)", (pessoa,))
        
        # Buscar o ID da Pessoa recém-inserida
        cursor.execute("SELECT Id FROM Pessoa WHERE Nome = ?", (pessoa,))
        pessoa_id = cursor.fetchone()[0]
        
        cursor.execute("""
                        INSERT INTO Bilhetes (PessoaId, cod_Bilhete, Destino, Origem, Data, Horario, Transportadora)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pessoa_id, '0', destino, origem, data, hora, transportadora))
        
# Salvar e fechar conexão
conn.commit()
conn.close()    