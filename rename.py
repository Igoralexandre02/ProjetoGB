import os
import re
import PyPDF2
import shutil

# Os parametros que decidem se o bilhete é IDA ou VOLTA devem ser definidos. 
# Defina o diretório onde estão os bilhetes
diretorio = r'C:\Users\05107553214\Documents\Bilhetes\PORTO VELHO'

# Cria uma pasta para armazenar as fotos, se não existir
fotos_folder = os.path.join(diretorio, "FOTOS")
os.makedirs(fotos_folder, exist_ok=True)

# Função para extrair informações do PDF
def extrair_informacoes(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text() or ""
                          
            # Captura o nome da transportadora
            transportadora = re.search(r'(SOLIMOES)', texto) # Procura no documento o nome "SOLIMOES"
            transportadora = re.search(r'(AMATUR)', texto)
            transportadora = transportadora.group(1) if transportadora else 'SERRA AZUL' # Caso não encontrado o primeiro nome "SOLIMOES", então "AMATUR" é a trasportadora
            
            if transportadora == 'AMATUR':                                                                         
                # Captura origem e destino e nome do passageiro
                # Transportadora AMATUR 
                origem = re.search(r'Origem:\s*\n\s*([A-ZÀ-ÿ\s-]+)(?=\s*-\s)', texto)
                texto_limpo = re.sub(r'[^A-Za-zÀ-ÿ\s\n]', '', texto)
                passageiro = re.search(r'Outros\s+\n\s*([A-ZÀ-ÿ\s]+)(?=\n)', texto_limpo)
            else:
                # Tranpostadora SOLIMOES
                origem = re.search(r'Origem:\s*([^\(]+)', texto)
                #destino = re.search(r'Destino:\s*([^\(]+)', texto)
                passageiro = re.search(r'Passageiro:\s*DOC:\s*\d*\s*-\s*(.*)', texto)
                          
            if origem and passageiro:                
                origem = origem.group(1).strip().replace("\n", " ")
                #destino = destino.group(1).strip().replace("\n", " ")
                nome_passageiro = passageiro.group(1).strip().replace("\n", " ")
                return nome_passageiro, origem, transportadora    
            
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
    
    return None, None, None

# Dicionário para armazenar informações dos passageiros
passageiros = {}

# Percorre todos os arquivos PDF no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.endswith('.pdf'):
        caminho_pdf = os.path.join(diretorio, arquivo)
        nome_passageiro, origem, transportadora = extrair_informacoes(caminho_pdf) 
        
        with open(caminho_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text() or ""
        
        if texto == '':                
            # Mover arquivo para a pasta de FOTOS
            shutil.move(caminho_pdf, os.path.join(fotos_folder, os.path.basename(caminho_pdf)))
            print('Movido com sucesso!')                          
        
        if nome_passageiro and origem:
            nomes = nome_passageiro.split()
            primeiro_nome = nomes[0]  # Primeiro nome
            segundo_nome = nomes[1] if len(nomes) > 1 else ""  # Segundo nome (se existir)
            terceiro_nome = nomes[2] if len(nomes) > 2 else ""  # Terceiro nome (se existir)
            quarto_nome = nomes[3] if len(nomes) > 3 else "" # Quarto nome (se existir)
            
            # Define tipo de bilhete com base na origem e destino
            tipo_bilhete = "Desconhecido"
            
            if origem == 'PORTO VELHO':
                tipo_bilhete = 'IDA'
            else :
                tipo_bilhete = 'VOLTA'
                   
            chave = (primeiro_nome, segundo_nome, terceiro_nome, quarto_nome, tipo_bilhete)
            
            if chave not in passageiros:
                passageiros[chave] = []
            passageiros[chave].append(arquivo)

# Função para gerar um nome único para o arquivo
def gerar_nome_unico(diretorio, novo_nome):
    contador = 1
    nome_final = novo_nome
    while os.path.exists(os.path.join(diretorio, nome_final)):
        nome_final = f"{novo_nome[:-4]}_{contador}.pdf"
        contador += 1
    return nome_final

# Renomeia os arquivos
for (primeiro_nome, segundo_nome, terceiro_nome, quarto_nome, tipo_bilhete), arquivos in passageiros.items():
    for arquivo in arquivos:
        if segundo_nome.upper() in {"DE", "DA", "DO"}:
            novo_nome = f"{primeiro_nome} {terceiro_nome} {quarto_nome}-{tipo_bilhete}.pdf".strip()  # Usa o quarto nome
        else:
            novo_nome = f"{primeiro_nome} {segundo_nome} {terceiro_nome}-{tipo_bilhete}.pdf".strip()  # Usa o terceiro nome
        
        novo_nome_unico = gerar_nome_unico(diretorio, novo_nome)
        
        caminho_antigo = os.path.join(diretorio, arquivo)
        caminho_novo = os.path.join(diretorio, novo_nome_unico)
        os.rename(caminho_antigo, caminho_novo)
        
        #print(f"Tentando renomear: {caminho_antigo} -> {caminho_novo}")  # Para depuração
        
        # Renomeia o arquivo
        #print(f'Renomeado: {arquivo} -> {novo_nome_unico}')
        
print('Sucesso')