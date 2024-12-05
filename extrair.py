import re
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

def extrair_nomes_fatura(fatura_arquivo):
    """Extrai os códigos do arquivo fatura.txt considerando múltiplos padrões."""
    codigosFatura = set()
    with open(fatura_arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()
        
        codigoFatura = re.findall(r"(?<=\b2024\s)\b(?=[A-Z0-9]*[0-9])[A-Z0-9]{5}\b", texto)
        
        # Adicionar códigos ao conjunto, removendo espaços desnecessários
        codigosFatura.update(n.strip() for n in codigoFatura if n.strip())
        
    return codigosFatura

def marcar_codigos_no_pdf(pdf_entrada, pdf_saida, codigos, cor=(0.8, 0.9, 1)):
    """
    Marca os códigos encontrados no PDF com uma sobreposição azul-claro.
    
    Args:
        pdf_entrada (str): Caminho do PDF original.
        pdf_saida (str): Caminho do PDF de saída.
        codigos (set): Conjunto de códigos a serem marcados.
        cor (tuple): Cor RGB para o destaque (padrão: azul-claro).
    """
    reader = PdfReader(pdf_entrada)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        # Extrair texto da página
        texto = page.extract_text()
        
        # Criar um buffer para sobreposição
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=page.mediabox)
        
        # Verificar se algum código está presente e marcá-lo
        encontrou = False
        for codigo in codigos:
            if codigo in texto:
                encontrou = True
                # Localizar a posição do código (ajustar para PDFs reais)
                x, y = 100, 500  # Coordenadas fictícias; ajustar conforme o caso real
                largura, altura = 200, 20
                
                can.setFillColorRGB(*cor)
                can.rect(x, y, largura, altura, fill=True)
        
        can.save()
        packet.seek(0)

        # Adicionar a sobreposição somente se houve algum código
        if encontrou:
            overlay_reader = PdfReader(packet)
            overlay_page = overlay_reader.pages[0]  # Primeira página do buffer
            page.merge_page(overlay_page)
        
        writer.add_page(page)
    
    # Salvar o PDF com os destaques
    with open(pdf_saida, "wb") as f:
        writer.write(f)

# Caminhos dos arquivos
bilhetes_pdf = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes_juntos.pdf'
fatura_arquivo = r'C:\Users\igora\OneDrive\Documents\Bilhetes\fatura.txt'
pdf_saida = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes_marcados.pdf'

# Extrair códigos da fatura
codigosFatura = extrair_nomes_fatura(fatura_arquivo)

# Marcar os códigos encontrados no PDF
marcar_codigos_no_pdf(bilhetes_pdf, pdf_saida, codigosFatura)
