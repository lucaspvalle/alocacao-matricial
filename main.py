from ortools.linear_solver import pywraplp
import pandas as pd

# Importação
df = pd.read_csv("input/formulario.csv", encoding="unicode_escape", sep=";")  # interesses dos membros
limites = pd.read_csv("input/times.csv", encoding="unicode_escape", sep=";", index_col=0).T  # MaxMin por time
exceto = pd.read_csv("input/exceto.csv", encoding="unicode_escape", sep=";")  # não entra no domínio

# Pré-processamento
df = (df
      .replace([3, 4], [1000, 10000])
      .melt(id_vars="Nome", var_name="Time", value_name="Interesse")
      .merge(exceto, left_on=["Nome", "Time"], right_on=["Nome", "Fixo"], how="outer")
      .merge(limites, left_on=["Time"], right_index=True)
      .fillna(0))

# Solver
solver = pywraplp.Solver.CreateSolver("Alocação de Membros", "CBC")

# Variável de decisão
df["X"] = df.apply(lambda r: solver.BoolVar(f"X_{r.Nome}_{r.Time}") if not r["Fixo"] else 1, axis=1)

# Função Objetivo
solver.Minimize(solver.Sum(df["Interesse"] * df["X"]))

# O membro deve ser alocado em apenas uma área
(df
 .query('~ Time.str.contains("Proj.")')
 .groupby('Nome')
 .apply(lambda r: solver.Add(r['X'].sum() == 1, f"aloca_areas_{r.iloc[0].Nome}")))

# O membro deve ser alocado em apenas um projeto
(df
 .query('~ Time.str.contains("Área")')
 .groupby('Nome')
 .apply(lambda r: solver.Add(solver.Sum(r['X']) == 1, f"aloca_projetos_{r.iloc[0].Nome}")))

# O time (área ou projeto) possui um número máximo de membros
(df
 .groupby("Time")
 .apply(lambda r: solver.Add(solver.Sum(r['X']) <= r.iloc[0]['Max'], f"limite_max_{r.iloc[0].Time}")))

# O time (área ou projeto) possui um número mínimo de membros
(df
 .groupby("Time")
 .apply(lambda r: solver.Add(solver.Sum(r['X']) >= r.iloc[0]['Min'], f"limite_min_{r.iloc[0].Time}")))

# Resolvendo
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Valor objetivo:', solver.Objective().Value())
else:
    print('Não há solução factível!')

# Imprimindo resultados
df["sol"] = df.apply(lambda r: r['X'].value() if not r['X'] == 1 else 1, axis=1)
df.to_csv("output/solucao.csv", columns=["Nome", "Time"], index=False)
