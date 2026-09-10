# %%
import pandas as pd
# %%

base = pd.read_csv("../data/dados_processados/base_analitica.csv",
                   parse_dates=[
                           "Order Date",
                           "Delivery Date",
                           "Birthday",
                           "Open Date"
                       ])

base.head()

# %%

faturamento_total = base["Receita USD"].sum()
custo_total = base["Custo USD"].sum()
lucro_total = base["Lucro USD"].sum()

quantidades_vendidas = base["Quantity"].sum()
total_pedidos = base["Order Number"].nunique()
ticket_medio = faturamento_total / total_pedidos

# %%

print(f"Faturamento Total: US$ {faturamento_total:,.2f}")
print(f"Custo Total: US$ {custo_total:,.2f}")
print(f"Lucro Total: US$ {lucro_total:,.2f}")
print(f"Quantidades Vendida: {quantidades_vendidas:,}")
print(f"Total de Pedidos: {total_pedidos:,}")
print(f"Ticket Médio: US$ {ticket_medio:,.2f}")

# %%
base["Ano"] = base["Order Date"].dt.year

base.head()
# %%

faturamento_ano = (
    base[base["Ano"] < 2021]
    .groupby("Ano")["Receita USD"]
    .sum()
    .reset_index()
)

print(faturamento_ano)

# %%

print("Primeira venda:", base["Order Date"].min())
print("Última venda:", base["Order Date"].max())

# %%

faturamento_ano["Crescimento %"] = (
    faturamento_ano["Receita USD"].pct_change() * 100
)

print(faturamento_ano)
# %%

base["Mes"] = base ["Order Date"].dt.month
# %%

faturamento_mensal = (
    base[base["Ano"].isin([2019,2020])]
    .groupby(["Ano","Mes"])["Receita USD"]
    .sum()
    .reset_index()
)

faturamento_mensal
# %%

faturamento_mensal["Crescimento %"] = (
    faturamento_mensal["Receita USD"].pct_change() * 100
)

print(faturamento_mensal)
# %%
comparacao = faturamento_mensal.pivot(
    index="Mes",
    columns="Ano",
    values="Receita USD"
)

print(comparacao)

# %%
comparacao["Variacao %"] = (
    (comparacao[2020] - comparacao[2019]) / comparacao[2019]
) * 100

print(comparacao)

# %%

base["Canal"] = base["StoreKey"].apply(
    lambda x: "Online" if x == 0 else "Loja Física"
)

base.head()
# %%
print(base["Canal"].value_counts())

# %%

faturamento_canal = (
    base[base["Ano"].isin([2019,2020])]
    .groupby(["Ano", "Canal"])["Receita USD"]
    .sum()
    .reset_index()
)

print(faturamento_canal)
# %%

comparacao_canal = faturamento_canal.pivot(
    index="Canal",
    columns="Ano",
    values="Receita USD"
)

print(comparacao_canal)

# %%

comparacao_canal["Variacao %"] = (
    (comparacao_canal[2020] - comparacao_canal[2019])
    / comparacao_canal[2019]
) * 100

print (comparacao_canal)