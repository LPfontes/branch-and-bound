from mip import *
from modulo_Problema_linear import Problema_linear
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            tamanho_da_lista = len(linhas)
            lista_restricoes = []
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
        
        return quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes
    except FileNotFoundError:
        print(f'O arquivo "{nome_arquivo}" não foi encontrado.')


nome_arquivo = 'teste2.txt'  
quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes = ler_arquivo(nome_arquivo)
problema = Problema_linear(nome_arquivo,quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes) 
problema.adicionar_restricao(problema.model.vars[0],1,"==","nova_cost")
problema.salvar_modelo()
problema.exibir_modelo()
problema.remover_restricao(problema.model.constr_by_name("nova_cost"))
problema.salvar_modelo()
problema.exibir_modelo()








    
