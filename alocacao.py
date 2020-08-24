import pandas as pd
import pulp

#importando dados
interesse = pd.read_csv ("respostas.csv", encoding = "unicode_escape", sep = ";")
membros = pd.read_csv ("membros.csv", encoding = "unicode_escape", sep = ";")
prealoc = pd.read_csv ("pre alocados.csv", encoding = "unicode_escape", sep = ";")

#formatando as tabelas
interesse.set_index (interesse.columns [0], inplace = True)
membros.set_index (membros.columns [0], inplace = True)

#atualizando valores de 3 e 4 por valores muito grandes para evitar a alocação com este interesse
interesse.replace ([3, 4], [1000, 10000], inplace = True)

#modelo
#criando variáveis binárias de decisão para o membro m ser alocado no time t
var = pulp.LpVariable.dicts ("x", ((m,t) for m in interesse.index for t in interesse.columns), cat = "Binary")

#inicializando o modelo a fim de minimizar a função objetivo
model = pulp.LpProblem ("Alocacao", pulp.LpMinimize)

#criando a função objetivo de x (m,t) * interesse (m,t)
model += pulp.lpSum (var [m,t] * interesse.loc [m,t] for m in interesse.index for t in interesse.columns), "Função Objetivo"

#guardando nomes de áreas, projetos e eventuais times fora da matriz
area = [t for t in interesse.columns if "Área" in t]
projeto = [t for t in interesse.columns if "Proj." in t]
fora = [t for t in interesse.columns if "Área" not in t and "Proj." not in t]

#guardando nomes e times nas quais as pessoas devem continuar
prealocados = [(prealoc.iloc [idx,0], prealoc.iloc [idx,1]) for idx in range (len (prealoc))]

#iterando os membros
for m in interesse.index:
    #alocação em uma área t para cada membro m
    model += pulp.lpSum (var [m,t] for t in area) + (var [m,t] for t in fora) == 1
    #alocação em um projeto t para cada membro m
    model += pulp.lpSum (var [m,t] for t in projeto) + (var [m,t] for t in fora) == 1
    
#iterando os times
for t in interesse.columns:
    #restrição máxima de membros em um time t
    model += pulp.lpSum (var [m,t] for m in interesse.index) <= membros.loc ["Max", t]
    #restrição mínima de membros em um time t
    model += pulp.lpSum (var [m,t] for m in interesse.index) >= membros.loc ["Min", t]

#iterando pessoas que vão continuar em um time que já estavam
for m,t in prealocados:
    model += pulp.lpSum (var [m,t]) == 1

model.solve()
print (pulp.LpStatus [model.status])
print (f"Valor objetivo: {pulp.value (model.objective)}")

resultado = [(m,t) for m in interesse.index for t in interesse.columns if var [m,t].value() == 1]

for m in interesse.index:
    alocacoes = [item [1] for item in resultado if item [0] == m]
    print (m, ": ", alocacoes [0], " e ", alocacoes [1])