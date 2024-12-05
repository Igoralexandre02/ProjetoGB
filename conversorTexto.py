import PyPDF2

# Função para ler um PDF e salvar em um arquivo texto
def pdf_para_texto(pdf_path, txt_path):
    # Abrindo o arquivo PDF
    with open(pdf_path, 'rb') as pdf_file:
        # Criando um objeto PDF Reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Criando ou abrindo um arquivo texto para escrita
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # Iterando pelas páginas do PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extraindo texto da página
                page = pdf_reader.pages[page_num]
                texto = page.extract_text()
                
                # Escrevendo o texto extraído no arquivo texto
                if texto:  # Verifica se o texto não é None
                    txt_file.write(texto)
                    #txt_file.write()  # Adiciona uma nova linha entre as páginas

# Exemplo de uso
pdf_path = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes_juntos.pdf'
txt_path = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes.txt'
pdf_para_texto(pdf_path, txt_path)

print("Conversão concluída!")
