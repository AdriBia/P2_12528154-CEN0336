#!/usr/bin/env python3

#importando a biblioteca sys para receber as informações na linha de comando
import sys

#definindo os códons de parada e o códon de início
CODONS_PARADA = {"TAA", "TAG", "TGA"}  #códons de parada
CODON_INICIO = "ATG"  #códon de início

#cria um dicionário de códons para aminoácidos
CODON_PARA_AMINOACIDO = {
    "ATA": "I", "ATC": "I", "ATT": "I", "ATG": "M",
    "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T",
    "AAC": "N", "AAT": "N", "AAA": "K", "AAG": "K",
    "AGC": "S", "AGT": "S", "AGA": "R", "AGG": "R",
    "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L",
    "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P",
    "CAC": "H", "CAT": "H", "CAA": "Q", "CAG": "Q",
    "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R",
    "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V",
    "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A",
    "GAC": "D", "GAT": "D", "GAA": "E", "GAG": "E",
    "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G",
    "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S",
    "TTC": "F", "TTT": "F", "TTA": "L", "TTG": "L",
    "TAC": "Y", "TAT": "Y", "TAA": "*", "TAG": "*",  # * é o código de parada
    "TGC": "C", "TGT": "C", "TGA": "*", "TGG": "W"
}

def traduzir_orf_em_peptideo(orf): #traduz um ORF em uma sequência de aminoácidos


    peptideo = ""  #armazena a sequência de aminoácidos traduzida
    for i in range(0, len(orf) - 2, 3):  #itera sobre os códons (3 bases por vez)
        codon = orf[i:i + 3]  #códon de 3 bases
        aminoacido = CODON_PARA_AMINOACIDO.get(codon, "")  #obtém o aminoácido correspondente ao códon
        if aminoacido == "*": #a tradução é interrompida ao encontrar um códon de parada ('*').
            break
        peptideo += aminoacido  #adiciona o aminoácido à sequência do peptídeo
    return peptideo

def encontrar_orf_mais_longo(sequencia): #encontra o ORF mais longo em uma sequência dada, considerando os 6 quadros de leitura possíveis.
    orf_mais_longo, melhor_quadro, melhor_inicio, melhor_fim = "", None, None, None

    #verificando os 3 quadros na sequência direta
    for quadro in range(3):
        orf, inicio, fim = encontrar_orf(sequencia[quadro:], quadro + 1)
        if len(orf) > len(orf_mais_longo):  #se o ORF encontrado for mais longo, atualiza
            orf_mais_longo, melhor_quadro, melhor_inicio, melhor_fim = orf, quadro + 1, inicio, fim

    #verificando os 3 quadros na sequência complementar reversa
    reverso = complementar_reverso(sequencia)
    for quadro in range(3):
        orf, inicio, fim = encontrar_orf(reverso[quadro:], quadro + 4)
        if len(orf) > len(orf_mais_longo):  #se o ORF encontrado for mais longo, atualiza
            orf_mais_longo, melhor_quadro, melhor_inicio, melhor_fim = orf, quadro + 4, inicio, fim

    return orf_mais_longo, melhor_quadro, melhor_inicio, melhor_fim


#procurando o ORF
def encontrar_orf(sequencia, quadro):

    orf, inicio, fim, dentro_orf = "", None, None, False
    for i in range(0, len(sequencia) - 2, 3):  #itera sobre a sequência de 3 em 3 bases
        codon = sequencia[i:i + 3]  #códon de 3 bases
        if codon == CODON_INICIO and not dentro_orf:  #encontra o início do ORF
            orf, dentro_orf, inicio = codon, True, i + 1 + (quadro - 1)
        elif dentro_orf:
            orf += codon  #adiciona o códon ao ORF
            if codon in CODONS_PARADA:  #termina o ORF
                fim = i + 3
                return orf, inicio, fim  #retorna o ORF, o início e o fim
    return orf, inicio, fim  #caso não encontre um códon de parada, retorna o ORF parcial

#gera a sequência complementar reversa de uma sequência
def complementar_reverso(sequencia):
    complemento = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(complemento.get(base, base) for base in reversed(sequencia))  # Inverte e substitui as bases


#lê o arquivo multifasta e armazena as sequências
def ler_multifasta(arquivo):
    try:
        with open(arquivo, 'r') as f:
            sequencias, cabecalho_atual = {}, None
            for linha in f:
                linha = linha.strip()  #remove espaços em branco da linha
                if linha.startswith(">"):  #se for um cabeçalho
                    cabecalho_atual = linha  #atualiza o cabeçalho
                    sequencias[cabecalho_atual] = ""  #cria uma chave para a sequência
                elif cabecalho_atual:
                    sequencias[cabecalho_atual] += linha  #adiciona a sequência à chave
            return sequencias
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        sys.exit(1)  #encerra o script com erro
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)  #encerra o script com erro

#salvando as sequencias em FASTA
def salvar_fasta(sequencias, arquivo):
    with open(arquivo, 'w') as f:
        for cabecalho, sequencia in sequencias.items():
            f.write(f"{cabecalho}\n")  #escreve o cabeçalho
            for i in range(0, len(sequencia), 60):
                f.write(f"{sequencia[i:i + 60]}\n")  #escreve a sequência dividida em blocos de 60 bases


#executa a função principal que executa todas as outras
def main():
    if len(sys.argv) != 2:  #verifica se o usuário forneceu todos os argumentos
        print("Uso: python script_getORF.py <arquivo_multifasta>")
        sys.exit(1)  #encerra o script com erro

    arquivo = sys.argv[1]  #obtém o nome do arquivo multifasta a partir dos argumentos
    sequencias = ler_multifasta(arquivo)  #lê as sequências do arquivo multifasta
    orfs, peptideos = {}, {}

    for cabecalho, sequencia in sequencias.items():
        orf, quadro, inicio, fim = encontrar_orf_mais_longo(sequencia)  #encontra o ORF mais longo

        if orf and quadro and inicio and fim:
            peptideo = traduzir_orf_em_peptideo(orf)  #traduz o ORF para um peptídeo
            novo_cabecalho = f"{cabecalho}_quadro{quadro}_{inicio}_{fim}"  #atualiza o cabeçalho
            orfs[novo_cabecalho] = orf  #armazena o ORF
            peptideos[novo_cabecalho] = peptideo  #armazena o peptídeo
        else:
            print(f"Aviso: Nenhum ORF encontrado para {cabecalho}")

    salvar_fasta(orfs, "ORF.fna")  #salva os ORFs em um arquivo FASTA
    salvar_fasta(peptideos, "ORF.faa")  #salva os peptídeos em um arquivo FASTA
    print("Processamento concluído. Os resultados foram salvos nos arquivos ORF.fna e ORF.faa.")  #mensagem final

if __name__ == "__main__":
    main()
