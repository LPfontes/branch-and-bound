from mip import *
class Problema_linear:
    def __init__(self,nome_arquivo, quantidade_variaveis,quantidade_restricoes,coeficientes_objetivo,lista_restricoes):
        self.model = Model(nome_arquivo,sense=MAXIMIZE, solver_name=CBC)
        x = {i: self.model.add_var(var_type=CONTINUOUS, name=f'x_{i}', lb=0.0) for i in  range(1,quantidade_variaveis+1)}
        self.model.objective = xsum(coeficientes_objetivo[i-1]*x[i] for i in range(1,quantidade_variaveis+1))
        for i in range(quantidade_restricoes):
            tamanho_lista = len(lista_restricoes[i])
            soma =  xsum(lista_restricoes[i][j]*x[j+1] for j in range (tamanho_lista-2))
            self.model +=soma <= lista_restricoes[i][tamanho_lista-1],"cost"+ str(i)
        print("Modelo criado")
        self.salvar_modelo()
        self.exibir_modelo()

    def salvar_modelo(self):  
        self.model.write("model.lp") 

    def exibir_modelo(self):  
        with open("model.lp") as f: # lê e exibe conteúdo do arquivo
            print(f.read())   

    def remover_restricao(self,restriçao):
        self.model.remove(restriçao)

    def adicionar_restricao(self, variavel, valor_restricao, tipo, nome):
        match tipo:
            case "<=":
                self.model.add_constr(variavel <= valor_restricao, nome)
            case ">=":
                self.model.add_constr(variavel >= valor_restricao, nome)
            case "==":
                self.model.add_constr(variavel == valor_restricao, nome)
            case _:
                raise ValueError("Tipo de restrição inválido. Use '<=', '>=', ou '=='.")
            
    def solve(model):
        status = model.optimize()
        print("Status = ",  status)
        print(f"Solution value  = {model.objective_value:.2f}\n")
        print("Solution:")
        for v in model.vars:
            print(f"{v.name} = {v.x:.2f}")
    