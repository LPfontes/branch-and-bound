from mip import *
from modulo_Problema_linear import Problema_linear
import copy
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

def todas_variaveis_inteiras(modelo):
        for var in modelo.modelo.vars:
            if abs(var.x - round(var.x)) >= 1e-6:
                return False
        return True   
    
def who_is_closer(modelo):
    var_prox_05 = None
    melhor_dist = 1000

    for v in modelo.modelo.vars:
        dist = abs(v.x - 0.5)

        if dist < melhor_dist:
            var_prox_05 = v
            melhor_dist = dist
 
    return var_prox_05

def branch_and_bound(problema):

    # Definimos um valor para a inicialização
    melhor_solucao = -float("inf")
    # Variável que guarda o melhor modelo encontrado
    melhor_problema = None
    # Inicializando uma fila com os modelos abertos
    fila = [problema]

    # Só para quando a fila estiver vazia
    while fila:
        # Modelo atual é sempre o primeiro elemento da fila
        problema_atual = fila[0]

        status = problema_atual.resolver()

        # Verifica se houve uma solução viável
        if status == OptimizationStatus.OPTIMAL:

            # Busca a variável mais próxima de 0.5
            var_prox_05 = who_is_closer(problema_atual)
            # Verifica se todas as variáveis são inteiras
            inteiro = todas_variaveis_inteiras(problema_atual)
            
            if inteiro:
                # Sendo todas inteiras, vemos se ela é a melhor solução atual
                if problema_atual.modelo.objective_value > melhor_solucao:
                    melhor_solucao = problema_atual.modelo.objective_value
                    melhor_problema = problema_atual
        
            else:
                # Não sendo inteira, criamos novas condições para solucionar o problema
                if problema_atual.modelo.objective_value > melhor_solucao:
        
                    model1 = Problema_linear(problema_atual.modelo.copy())
                    model1.adicionar_restricao(var_prox_05,1,">=","")
                    model2 = Problema_linear(problema_atual.modelo.copy())
                    model2.adicionar_restricao(var_prox_05,0,"<=","")

                    # Adicionamos os novos modelos a lista 
                    fila.append(model1)
                    fila.append(model2)

        # Removemos o modelo corrente da fila
        fila.pop(0)
    
    return  melhor_problema 
with open("saida.txt", "w") as arquivo:
    for i in range(1, 5):

        quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes = ler_arquivo(f"teste{i}.txt")
        problema = Problema_linear(None)
        problema.criarModelo(f"teste{i}.txt",CONTINUOUS,quantidade_variaveis,0.0,1.0,quantidade_restricoes,coeficientes_objetivo,lista_restricoes)

        solucao = branch_and_bound(problema)
   
        print(f"Solution Teste {i}  = {solucao.modelo.objective_value:.2f}", file=arquivo)
        arquivo.write("Solution:\n")
        for v in solucao.modelo.vars:
            print(f"{v.name} = {v.x:.2f}", file=arquivo)
        print("--------------------------------------------------", file=arquivo)




    
