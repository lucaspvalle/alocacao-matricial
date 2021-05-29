from ortools.linear_solver import pywraplp
import pandas as pd

# Importação
df = pd.read_csv("input/formulario.csv")  # interesses dos membros
limites = pd.read_csv("input/times.csv", index_col=0).T  # MaxMin por time
exceto = pd.read_csv("input/exceto.csv")  # não entra no domínio

# Pré-processamento
df = (df
      .replace([3, 4], [1000, 10000])
      .melt(id_vars="Nome", var_name="Time", value_name="Interesse")
      .merge(exceto, left_on=["Nome", "Time"], right_on=["Nome", "Fixo"], how="outer")
      .merge(limites, left_on=["Time"], right_index=True)
      .fillna(0))

df["Fixo"] = df["Fixo"] != 0  # Convertendo em booleano para restringir domínio

# Modelo
solver = pywraplp.Solver.CreateSolver("Alocação de Membros", "CBC")

# Variável de decisão
df["X"] = df.apply(lambda r: solver.BoolVar(f"X_{r.Nome}_{r.Time}") if not r["Fixo"] else 1, axis=1)

# Função Objetivo
solver.Minimize(solver.Sum(df.query('~ Fixo').apply(lambda r: r['Interesse'] * r['X'], axis=1)))

# O membro deve ser alocado em apenas uma área
(df
 .query('~ Time.str.contains("Proj.")')
 .groupby('Nome')
 .apply(lambda r: solver.Add(r['X'].sum() == 1, f"aloca_areas_{r.iloc[0].Nome}")))

# O membro deve ser alocado em apenas um projeto
(df
 .query('~ Time.str.contains("Area")')
 .groupby('Nome')
 .apply(lambda r: solver.Add(solver.Sum(r['X']) == 1, f"aloca_projetos_{r.iloc[0].Nome}")))


def limita_membros_no_time(r):
    solver.Add(solver.Sum(r['X']) <= r.iloc[0]['Max'], f"limite_max_{r.iloc[0].Time}")  # Limite máximo de membros
    solver.Add(solver.Sum(r['X']) >= r.iloc[0]['Min'], f"limite_min_{r.iloc[0].Time}")  # Limite mínimo de membros


# O time (área ou projeto) possui limites inferiores e superiores de membros
df.groupby("Time").apply(limita_membros_no_time)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Valor objetivo:', solver.Objective().Value())

    # Imprimindo resultados
    df["sol"] = df.apply(lambda r: r['X'].solution_value() if not r['Fixo'] else 1, axis=1)
    df.query('sol == 1').to_csv("output/solucao.csv", columns=["Nome", "Time"], index=False)

else:
    print('Não há solução!')
