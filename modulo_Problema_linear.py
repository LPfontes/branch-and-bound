from mip import *
class Problema_linear:
    def __init__(self,modelo):
        self.modelo = modelo
        
    def criarModelo(self,nome_arquivo,tipo_das_variaveis,quantidade_variaveis,lower_bound,upper_bound,quantidade_restricoes,coeficientes_objetivo,lista_restricoes):
        # Criação de um modelo de Maximização
        self.modelo = Model(nome_arquivo,sense=MAXIMIZE, solver_name=CBC)
        x = {i: self.modelo.add_var(var_type=tipo_das_variaveis, name=f'x_{i}', lb=lower_bound, ub=upper_bound) for i in  range(1,quantidade_variaveis+1)}
        
        self.modelo.objective = xsum(coeficientes_objetivo[i-1]*x[i] for i in range(1,quantidade_variaveis+1))

        for i in range(quantidade_restricoes):
            tamanho_lista = len(lista_restricoes[i])
            soma =  xsum(lista_restricoes[i][j]*x[j+1] for j in range (tamanho_lista-1))
            self.modelo += soma <= lista_restricoes[i][tamanho_lista-1]
        self.salvar_modelo()
        

    def salvar_modelo(self):  
        self.modelo.write("model.lp") 

    def exibir_modelo(self):  
        with open("model.lp") as f: # lê e exibe conteúdo do arquivo
            print(f.read())   

    def remover_restricao(self,restriçao):
        self.modelo.remove(restriçao)

    def adicionar_restricao(self, variavel, valor_restricao, tipo, nome):
        match tipo:
            case "<=":
                self.modelo.add_constr(variavel <= valor_restricao, nome)
            case ">=":
                self.modelo.add_constr(variavel >= valor_restricao, nome)
            case "==":
                self.modelo.add_constr(variavel == valor_restricao, nome)
            case _:
                raise ValueError("Tipo de restrição inválido. Use '<=', '>=', ou '=='.")
            
    def resolver(self):
        self.variaveis_not_integer = []
        status = self.modelo.optimize()
        if status == OptimizationStatus.OPTIMAL:
            for vars in self.modelo.vars:
                if not vars.x.is_integer():
                    self.variaveis_not_integer.append(vars) 
            
        return status
    