class Problema_linear:
    def __init__(self, quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes):
        self.quantidade_variaveis = quantidade_variaveis
        self.quantidade_restricoes = quantidade_restricoes
        self.coeficientes_objetivo = coeficientes_objetivo
        self.lista_restricoes = lista_restricoes
    
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            tamanho_da_lista = len(linhas)
            lista_restricoes = []
            # Salvando cada linha em uma variável
            for i in range(tamanho_da_lista):
                linha = linhas[i].split()
                match i:
                    case 0:
                        quantidade_variaveis = int(linha[0])
                        quantidade_restricoes = int(linha[1])
                    case 1:
                        coeficientes_objetivo = []
                        for variaveis in range(quantidade_variaveis):
                            coeficientes_objetivo.append(int(linha[variaveis]))
                    
                    case _:
                        tamanho_da_linha = len(linha)
                        lista = []
                        for restricao in range(tamanho_da_linha):
                            lista.append(int(linha[restricao]))
                        lista_restricoes.append(lista)
        problema = Problema_linear(quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes)    
        return problema
    except FileNotFoundError:
        print(f'O arquivo "{nome_arquivo}" não foi encontrado.')

# Exemplo de uso
nome_arquivo = 'teste1.txt'  # Substitua 'exemplo.txt' pelo nome do arquivo que deseja ler
problema = ler_arquivo(nome_arquivo)

    
