from mip import *
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

def Criar_modelo(problema):
    model = Model(sense=MAXIMIZE, solver_name=CBC)
    x = {i: model.add_var(var_type=CONTINUOUS, name=f'x_{i}', lb=0.0) for i in  range(1,problema.quantidade_variaveis+1)}
    model.objective = xsum(problema.coeficientes_objetivo[i-1]*x[i] for i in range(1,problema.quantidade_variaveis+1))
    for i in range(problema.quantidade_restricoes):
        tamanho_lista = len(problema.lista_restricoes[i])
        soma =  xsum(problema.lista_restricoes[i][j]*x[j+1] for j in range (tamanho_lista-2))
        model +=soma <= problema.lista_restricoes[i][tamanho_lista-1],"cost"+ str(i)
    model.write("model.lp") # salva modelo em arquivo
    with open("model.lp") as f: # lê e exibe conteúdo do arquivo
        print(f.read())
    return model

def remover_restricao(restriçao):
    model.remove(restriçao)

def adicionar_restriçao_menor(variavel,restricao,nome):
    model.add_constr(variavel <= restricao,nome)

def adicionar_restriçao_maior(variavel,restricao,nome):
    model.add_constr(variavel >= restricao,nome)

def adicionar_restriçao_igual(variavel,restricao,nome):
    model.add_constr(variavel == restricao,nome)


    
nome_arquivo = 'teste2.txt'  
problema = ler_arquivo(nome_arquivo)
model = Criar_modelo(problema)
adicionar_restriçao_menor(model.vars[1],1,"cost_nova")
model.write("model.lp") # salva modelo em arquivo
with open("model.lp") as f: # lê e exibe conteúdo do arquivo
    print(f.read())
remover_restricao(model.constr_by_name("cost_nova"))
model.write("model.lp") # salva modelo em arquivo
with open("model.lp") as f: # lê e exibe conteúdo do arquivo
    print(f.read())
adicionar_restriçao_igual(model.vars[3],1,"cost_nova")
model.write("model.lp") # salva modelo em arquivo
with open("model.lp") as f: # lê e exibe conteúdo do arquivo
    print(f.read())
remover_restricao(model.constr_by_name("cost_nova"))
model.write("model.lp") # salva modelo em arquivo
with open("model.lp") as f: # lê e exibe conteúdo do arquivo
    print(f.read())


    
