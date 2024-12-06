import re
import fitz  # PyMuPDF
from concurrent.futures import ThreadPoolExecutor

def extrair_nomes_fatura(fatura_arquivo):
    """Extrai os códigos do arquivo fatura.txt considerando múltiplos padrões."""
    codigosFatura = set()
    with open(fatura_arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()
        
        codigoFatura = re.findall(r"(?<=\b2024\s)\b(?=[A-Z0-9]*[0-9])[A-Z0-9]{5}\b", texto)
        
        # Adicionar códigos ao conjunto, removendo espaços desnecessários
        codigosFatura.update(n.strip() for n in codigoFatura if n.strip())
        
    return codigosFatura

def processar_pagina(args):
    page_num, page, codigos, cor = args
    texto = page.get_text("text").lower()
    encontrados = set()
    for codigo in codigos:
        if codigo in texto:
            areas = page.search_for(codigo)
            for area in areas:
                # Criar a anotação de destaque (highlight)
                annot = page.add_highlight_annot(area)
                if annot:
                    # Definir cor para o highlight
                    annot.set_colors(stroke=cor, fill=None)  # Cor de borda (stroke)
                    annot.update()  # Atualizar a anotação

                # Adicionar texto com o código na página
                texto_posicao = fitz.Rect(area.x0, area.y0 - 10, area.x1, area.y0)
                page.insert_textbox(texto_posicao, codigo, fontsize=8, color=cor)
                
                # Após a última linha de cada bilhete, adicionar "BILHETE VERIFICADO"
                # A última linha do bilhete é a linha do código, então pegamos a parte inferior da área
                ultima_linha_y = area.y1
                posicao_mensagem = fitz.Rect(area.x0, ultima_linha_y + 5, area.x1, ultima_linha_y + 20)  # Ajuste de posição
                page.insert_textbox(posicao_mensagem, "BILHETE VERIFICADO", fontsize=10, color=(1, 0, 0))  # Vermelho
            encontrados.add(codigo)
    return encontrados

def marcar_codigos_no_pdf_paralelo(pdf_entrada, pdf_saida, codigos, cor=(1, 0, 0)):
    """
    Marca os códigos encontrados no PDF e escreve os códigos na página.

    Args:
        pdf_entrada (str): Caminho do PDF original.
        pdf_saida (str): Caminho do PDF de saída.
        codigos (set): Conjunto de códigos a serem marcados.
        cor (tuple): Cor RGB normalizada para o destaque (valores entre 0 e 1).
    """
    doc = fitz.open(pdf_entrada)
    codigos_restantes = {codigo.strip().lower() for codigo in codigos}

    # Preparar argumentos para processamento paralelo
    args_list = [(i, page, codigos_restantes, cor) for i, page in enumerate(doc)]

    # Processar páginas em paralelo
    with ThreadPoolExecutor() as executor:
        resultados = executor.map(processar_pagina, args_list)

    # Atualizar códigos restantes com base nos resultados
    for encontrados in resultados:
        codigos_restantes -= encontrados

        # Encerrar se todos os códigos foram encontrados
        if not codigos_restantes:
            break

    # Salvar o PDF com destaques
    doc.save(pdf_saida)
    doc.close()

# Caminhos dos arquivos
bilhetes_pdf = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes_juntos.pdf'
fatura_arquivo = r'C:\Users\igora\OneDrive\Documents\Bilhetes\fatura.txt'
pdf_saida = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes_marcados.pdf'

# Extrair códigos da fatura
codigosFatura = extrair_nomes_fatura(fatura_arquivo)

# Marcar os códigos encontrados no PDF
marcar_codigos_no_pdf_paralelo(bilhetes_pdf, pdf_saida, codigosFatura)
