# %%
import pandas as pd
from matplotlib.ticker import FuncFormatter
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
# %%

pedidos_por_ano = (
    base.groupby("Ano")["Order Number"].nunique()
)

print(pedidos_por_ano)
# %%

variacao_pedidos = (
    (pedidos_por_ano[2020] - pedidos_por_ano[2019]) / pedidos_por_ano[2019]
) * 100

print(f"Variação de pedidos 2019 -> 2020: {variacao_pedidos:.2f} %")

# %%
receita_por_pedido = (
    base
    .groupby(["Ano", "Order Number"])["Receita USD"]
    .sum()
    .reset_index()
)

receita_por_pedido.head()
# %%

ticket_medio_ano = (
    receita_por_pedido
    .groupby("Ano")["Receita USD"]
    .mean()
)

print(ticket_medio_ano)
# %%

variacao_ticket = (
    (ticket_medio_ano[2020] - ticket_medio_ano[2019]) / ticket_medio_ano[2019]
) * 100

print(f"Variação do ticket médio 2019 -> 2020: {variacao_ticket:.2f}%")
# %%

itens_por_pedido = (
    base
    .groupby(["Ano", "Order Number"])["Quantity"]
    .sum()
    .reset_index()
)

itens_por_pedido.head()
# %%

media_itens_por_pedido = (
    itens_por_pedido
    .groupby("Ano")["Quantity"]
    .mean()
)

print(media_itens_por_pedido)
# %%

variacao_itens = (
    (media_itens_por_pedido[2020] - media_itens_por_pedido[2019]) / media_itens_por_pedido[2019]
) * 100

print(f"Variação de itens por pedido 2019 -> 2020: {variacao_itens:.2f}%")
# %%

clientes_por_ano = (
    base
    .groupby("Ano")["CustomerKey"]
    .nunique()
)

print(clientes_por_ano)

# %%
variacao_clientes = (
    (clientes_por_ano[2020] - clientes_por_ano[2019]) / clientes_por_ano[2019]
) * 100

print(f"Variação de clientes 2019 -> 2020: {variacao_clientes:.2f}")
# %%

pedidos_por_cliente = pedidos_por_ano / clientes_por_ano

print(pedidos_por_cliente)

# %% 

variacao_pedidos_cliente = (
    (pedidos_por_cliente[2020] - pedidos_por_cliente[2019])
    / pedidos_por_cliente[2019]
) * 100

print(f"Variação de pedidos por cliente 2019 -> 2020: {variacao_pedidos_cliente:.2f}%")

# Análise Queda na receita 2020 -- FIM

# %%

receita_categoria = (
    base
    .groupby("Category")["Receita USD"]
    .sum()
    .sort_values(ascending=False)
)

print(receita_categoria)
# %%

receita_total = receita_categoria.sum()

# %%

participacao_categoria = (receita_categoria / receita_total) * 100

print(participacao_categoria)

# %%

lucro_categoria = (
    base
    .groupby("Category")["Lucro USD"]
    .sum()
    .sort_values(ascending=False)
)

print(lucro_categoria)


# %%

margem_categoria = (lucro_categoria/receita_categoria) * 100

print(margem_categoria.sort_values(ascending=False))

# %%

receita_produto = (
    base
    .groupby("Product Name")["Receita USD"]
    .sum()
    .sort_values(ascending=False)    
)

top10_receita_produto = receita_produto.head(10)

print(top10_receita_produto)
# %%

lucro_produto = (
    base
    .groupby("Product Name")["Lucro USD"]
    .sum()
)

print(lucro_produto)
# %%

analise_produtos = pd.DataFrame({
    "Receita USD": receita_produto,
    "Lucro USD": lucro_produto
})

analise_produtos.head()

# %%

analise_produtos["Margem %"] = (

    analise_produtos["Lucro USD"] / analise_produtos["Receita USD"]
) * 100

analise_produtos.head()

# %%

top10_produtos = (
    analise_produtos
    .sort_values("Receita USD", ascending=False)
    .head(10)
)

print(top10_produtos)

# %%

print(analise_produtos["Margem %"].describe())

# %%

correlacao = analise_produtos["Receita USD"].corr(
    analise_produtos["Margem %"]
)

print(correlacao)

# %%

import matplotlib.pyplot as plt

plt.scatter(
    analise_produtos["Receita USD"],
    analise_produtos["Margem %"],
    alpha=0.5
)

plt.xlabel("Receita USD")
plt.ylabel("Margem (%)")
plt.title("Relação entre Receita e Margem por Produto")

plt.show()

# %%

def classificar_margem(margem):
    if margem < 52:
        return "Baixa"
    elif margem < 60:
        return "Média"
    else:
        return "Alta"

analise_produtos["Faixa Margem"] = (
    analise_produtos["Margem %"]
    .apply(classificar_margem)
)

# %%

analise_produtos = analise_produtos.reset_index()

print(analise_produtos.head())

# %%
categoria_produto = (
    base
    .drop_duplicates("Product Name")
    .set_index("Product Name")["Category"]
)

print(categoria_produto)

# %%

analise_produtos["Category"] = (
    analise_produtos["Product Name"]
    .map(categoria_produto)
)

# %%
print(analise_produtos.head())
# %%
faixa_por_categoria = pd.crosstab(
    analise_produtos["Category"],
    analise_produtos["Faixa Margem"]
)

print(faixa_por_categoria)
# %%
faixa_por_categoria_pct = (
    faixa_por_categoria
    .div(faixa_por_categoria.sum(axis=1), axis=0)
    * 100
)

print(faixa_por_categoria_pct.round(2))
# %%

print(base.columns.tolist())

# %%

receita_por_pais = (
    base
    .groupby("Customer Country")["Receita USD"]
    .sum()
    .sort_values(ascending=False)
)

print(receita_por_pais)

# %%

participacao_pais = (receita_por_pais / receita_total) * 100

print(participacao_pais)

# %%

clientes_por_pais = (
    base
    .groupby("Customer Country")["CustomerKey"]
    .nunique()
    .sort_values(ascending=False)
)

print(clientes_por_pais)

# %%

participacao_cliente_pais = (clientes_por_pais / clientes_por_pais.sum()) * 100

print(participacao_cliente_pais)

# %%

receita_media_cliente_pais = receita_por_pais / clientes_por_pais

print(receita_media_cliente_pais.sort_values(ascending=False))

# %%

pedidos_por_pais = (
    base
    .groupby("Customer Country")["Order Number"]
    .nunique()
    .sort_values(ascending=False)
)

print(pedidos_por_pais)
# %%
pedidos_por_cliente_pais = (
    pedidos_por_pais / clientes_por_pais
) 

print(pedidos_por_cliente_pais.sort_values(ascending=False))
# %%

ticket_medio_pais = (receita_por_pais / pedidos_por_pais)

print(ticket_medio_pais.sort_values(ascending=False))

# Analise geografica --FIM

# %%

receita_por_cliente = (
    base
    .groupby("CustomerKey")["Receita USD"]
    .sum()
    .sort_values(ascending=False)
)

print(receita_por_cliente.head(10))
# %%

participacao_top10_clientes = (
    receita_por_cliente.head(10).sum() / receita_por_cliente.sum()
) * 100

print(participacao_top10_clientes)
# %%

total_clientes = receita_por_cliente.shape[0]

print(total_clientes)
# %%

qtd_top10_pct = int(total_clientes * 0.10)

print(qtd_top10_pct)

# %%

receita_por_cliente.head(qtd_top10_pct)


# %%

participacao_top10_pct = (
    receita_por_cliente.head(qtd_top10_pct).sum() / receita_por_cliente.sum()
    ) * 100

print(participacao_top10_pct)
# %%

pedidos_por_cliente_total = (
    base
    .groupby("CustomerKey")["Order Number"]
    .nunique()
    .sort_values(ascending=False)
)

print(pedidos_por_cliente_total.value_counts().sort_index())
# %%

clientes_compra_unica = (
    pedidos_por_cliente_total == 1
).sum()


clientes_recorrentes = (
    pedidos_por_cliente_total > 1
).sum()

print(clientes_compra_unica)
print(clientes_recorrentes)

# %%

pct_compra_unica = (
    clientes_compra_unica / total_clientes
) * 100

pct_recorrentes = (
    clientes_recorrentes / total_clientes
) * 100

print(f"Porcentagem clientes de compra única: {pct_compra_unica:.2f}%")
print(f"Porcentagem clientes recorrentes: {pct_recorrentes:.2f}%")


# %%

base["Tipo Cliente"] = base["CustomerKey"].map(
    lambda cliente: (
        "Compra Única"
        if pedidos_por_cliente_total[cliente] == 1
        else "Recorrente"
    )
)

# %%

print(
    base[["CustomerKey", "Tipo Cliente"]]
    .drop_duplicates()
    ["Tipo Cliente"]
    .value_counts()
)
# %%

receita_tipo_cliente = (
    base
    .groupby("Tipo Cliente")["Receita USD"]
    .sum()
    .sort_values(ascending=False)
)

print(receita_tipo_cliente)
# %%

pct_receita_tipo_cliente = (
    receita_tipo_cliente / receita_tipo_cliente.sum()
) * 100

print (pct_receita_tipo_cliente)


# %%

receita_media_recorrente = (
    receita_tipo_cliente["Recorrente"] / clientes_recorrentes
) 

receita_media_compra_unica = (
    receita_tipo_cliente["Compra Única"] / clientes_compra_unica
)

print(f"Receita média por cliente Compra Única: {receita_media_compra_unica:,.2f}")
print(f"Receita média por cliente Recorrente: {receita_media_recorrente:,.2f}")

# %%

vezes_maior_recorrente = receita_media_recorrente / receita_media_compra_unica

print(f"Cliente recorrente gera {vezes_maior_recorrente:.2f}x mais receita")

# %%

receita_por_ano = (
    base
    .groupby("Ano")["Receita USD"]
    .sum()
)

print(receita_por_ano)
# %%


def formatar_milhoes(x, pos):
    return f"US$ {x / 1_000_000:.0f} mi"

grafico_receita_por_ano = receita_por_ano.plot(
    kind="bar",
    figsize=(10, 5),
    title="Receita por Ano",
    xlabel="Ano",
    ylabel="Receita"
)

grafico_receita_por_ano.yaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.savefig("../visualizacoes/receita_por_ano.png", bbox_inches="tight")

plt.show()

# %%

comparacao_canal_grafico = (
    base[base["Ano"].isin([2019, 2020])]
    .groupby(["Canal", "Ano"])["Receita USD"]
    .sum()
    .unstack()
)

print(comparacao_canal_grafico)


# %%

comparacao_canal_grafico = comparacao_canal_grafico.plot(
    kind="bar",
    figsize=(10, 5),
    title="Receita por Canal — 2019 vs 2020",
    xlabel="Canal",
    ylabel="Receita"
)

comparacao_canal_grafico.yaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.xticks(rotation=0)
plt.legend(title="Ano")

plt.savefig("../visualizacoes/comparacao_canal_2019_2020.png", bbox_inches="tight")

plt.show()




# %%
grafico_receita_categoria = receita_categoria.plot(
    kind="barh",
    figsize=(10, 6),
    title="Receita por Categoria",
    xlabel="Receita"
)

grafico_receita_categoria.xaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.savefig("../visualizacoes/receita_categoria.png", bbox_inches="tight")

plt.show()


# %%

grafico_receita_por_pais = receita_por_pais.plot(
    kind="barh",
    figsize=(10, 6),
    title="Receita por País",
    xlabel="Receita",
    ylabel="País do Cliente"
)

grafico_receita_por_pais.xaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.savefig("../visualizacoes/receita_pais.png", bbox_inches="tight")

plt.show()


# %%

grafico_receita_tipo_cliente = receita_tipo_cliente.plot(
    kind="bar",
    figsize=(8, 5),
    title="Receita por Tipo de Cliente",
    xlabel="Tipo de Cliente",
    ylabel="Receita"
)

grafico_receita_tipo_cliente.yaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.xticks(rotation=0)

for i, valor in enumerate(receita_tipo_cliente):
    percentual = pct_receita_tipo_cliente.iloc[i]
    grafico_receita_tipo_cliente.text(
        i,
        valor,
        f"{percentual:.1f}%",
        ha="center",
        va="bottom"
    )

plt.savefig("../visualizacoes/receita_tipo_cliente.png", bbox_inches="tight")

plt.show()


# %%
grafico_top_10_produtos = top10_receita_produto.plot(
    kind="barh",
    figsize=(10, 6),
    title="Top 10 Produtos por Receita",
    xlabel="Receita"
)

grafico_top_10_produtos.xaxis.set_major_formatter(FuncFormatter(formatar_milhoes))

plt.savefig("../visualizacoes/top_10_produtos_por_receita.png", bbox_inches="tight")

plt.show()


# %%
