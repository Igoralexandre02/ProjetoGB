import re

def extrair_nomes_bilhetes(arquivo):
    """Extrai o codigo do bilhete do arquivo bilhetes.txt com o padrão específico."""
    
    codigosBilhete = set()
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()
        
        # Captura todos os codigos de uma vez
        match = re.findall(r'Passageiro:\s*DOC:\s*\d*\s*-\s*(.*)', texto)
        
        # Adiciona os codigos um conjuto    
        codigosBilhete.update(n.strip() for n in match)
        
        # Conta a quantidade de codigos encontrados
        quantidadeCodigos = len(match)
        codigosBilhete.add(f"1-Total: {str(quantidadeCodigos)}")
        
    return codigosBilhete

def extrair_nomes_fatura(arquivo):
    """Extrai os codigos do arquivo fatura.txt considerando múltiplos padrões."""
    codigosFatura = set()
    with open(arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()
        
        # Procurar nomes após 'Classe do Voo:'
        #padrao_classe_voo = r'Classe do Voo:\s*(?:\n|\s)*([A-Za-zÀ-ÖØ-öø-ÿ ]+)'
        
        codigoFatura = re.findall(r"(?<=\b2024\s)\b(?=[A-Z0-9]*[0-9])[A-Z0-9]{5}\b", texto)
        
        # Procurar nomes após 'Observação' e excluir 'EUCATUR' e padrões como 'ND00029561'
        #padrao_observacao = r'Observação:\s*(?:\n|\s)*([A-Za-zÀ-ÖØ-öø-ÿ ]+)(?!\s*EUCATUR|ND\d+|\b[A-Z]{2,}\d+)'
        #nomes_observacao = re.findall(padrao_observacao, texto)
        
        # Adicionar nomes ao conjunto, removendo espaços desnecessários
        codigosFatura.update(n.strip() for n in codigoFatura if n.strip())
        quantidadeFatura = len(codigoFatura)
        codigosFatura.add(f"Total: {str(quantidadeFatura)}")
        
    return codigosFatura

def comparar_nomes(bilhetes_arquivo, fatura_arquivo):
    """Compara os nomes dos passageiros nos arquivos de bilhetes e faturas."""
    nomes_bilhetes = extrair_nomes_bilhetes(bilhetes_arquivo)
    nomes_fatura = extrair_nomes_fatura(fatura_arquivo)

    # Identificar nomes em bilhetes que não estão nas faturas
    nomes_sem_fatura = nomes_bilhetes - nomes_fatura
    nomes_sem_bilhetes = nomes_fatura - nomes_bilhetes 
    
    return nomes_sem_fatura, nomes_sem_bilhetes

def salvar_nomes_ausentes(nomes_fatura, nomes_bilhete, arquivo_fatura, arquivo_bilhete):
    """Salva os nomes ausentes em um arquivo de saída."""
    with open(arquivo_fatura, 'w', encoding='utf-8') as f:
        f.write(f"Faturas sem bilhetes:\n")
        for nome in sorted(nomes_fatura):
            f.write(f"{nome}\n")
            
    with open(arquivo_bilhete, 'w', encoding='utf-8') as b:
        b.write(f"Bilhetes sem faturas:\n\n")    
        for nome in sorted(nomes_bilhete):
            b.write(f"{nome}\n")
            
# Defina os caminhos dos arquivos
bilhetes_arquivo = r'C:\Users\igora\OneDrive\Documents\Bilhetes\bilhetes.txt'
fatura_arquivo = r'C:\Users\igora\OneDrive\Documents\Bilhetes\fatura.txt'
arquivo_fatura = r'C:\Users\igora\OneDrive\Documents\Bilhetes\nomes_fatura.txt'
arquivo_bilhete = r'C:\Users\igora\OneDrive\Documents\Bilhetes\nomes_bilhetes.txt'

# Comparar e salvar nomes ausentes
nomes_sem_fatura, nomes_sem_bilhetes = comparar_nomes(bilhetes_arquivo, fatura_arquivo)
salvar_nomes_ausentes(nomes_sem_fatura, nomes_sem_bilhetes, arquivo_fatura, arquivo_bilhete)

print(f"Nomes ausentes foram salvos nos arquivos: nomes_fatura e nomes_bilhete")