import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)

base = pd.read_csv(
    "data/dados_processados/base_analitica.csv"
)

faturamento_total = base["Receita USD"].sum()
lucro_total = base["Lucro USD"].sum()
total_pedidos = base["Order Number"].nunique()
total_clientes = base["CustomerKey"].nunique()

margem_total = (lucro_total / faturamento_total) * 100

st.title("📊 Sales Analytics")
st.subheader("Resultados da análise")

st.markdown(
    "Visão geral dos principais resultados encontrados durante "
    "a análise dos dados de vendas."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Receita Total",
        value=f"US$ {faturamento_total / 1_000_000:.2f} mi"
    )

with col2:
    st.metric(
        label="🛒 Pedidos",
        value=f"{total_pedidos:,}"
    )

with col3:
    st.metric(
        label="👥 Clientes",
        value=f"{total_clientes:,}"
    )

with col4:
    st.metric(
        label="📈 Margem",
        value=f"{margem_total:.2f}%"
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📈 Receita por Ano")
    st.image(
        "visualizacoes/receita_por_ano.png",
        use_container_width=True
    )

with col2:
    st.subheader("🛒 Receita por Canal — 2019 × 2020")
    st.image(
        "visualizacoes/comparacao_canal_2019_2020.png",
        use_container_width=True
    )

with col3:
    st.subheader("🏷️ Receita por Categoria")
    st.image(
        "visualizacoes/receita_categoria.png",
        use_container_width=True
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌎 Receita por País")
    st.image(
        "visualizacoes/receita_pais.png",
        use_container_width=True
    )

with col2:
    st.subheader("👥 Receita por Tipo de Cliente")
    st.image(
        "visualizacoes/receita_tipo_cliente.png",
        use_container_width=True
    )

with col3:
    st.subheader("📦 Top 10 Produtos por Receita")
    st.image(
        "visualizacoes/top_10_produtos_por_receita.png",
        use_container_width=True
    )

st.markdown("---")

st.header("💡 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📉 Queda em 2020**

    A receita caiu aproximadamente **49% em 2020**, acompanhada
    por uma redução semelhante no número de pedidos.
    """)

    st.markdown("""
    **👥 Clientes recorrentes**

    Clientes recorrentes representam cerca de **61% da base**,
    mas são responsáveis por mais de **82% da receita**.
    """)

    st.markdown("""
    **🏷️ Categorias**

    As categorias **Computers** e **Home Appliances** concentram
    aproximadamente **54% da receita**.
    """)

with col2:
    st.markdown("""
    **🌎 Mercado**

    Os **Estados Unidos** representam aproximadamente **54% da receita**,
    sendo o principal mercado da análise.
    """)

    st.markdown("""
    **📦 Produtos**

    Os produtos de maior receita estão concentrados principalmente
    nas categorias de **computadores e televisores**.
    """)

    st.markdown("""
    **💰 Rentabilidade**

    As margens das categorias são relativamente equilibradas,
    apesar das diferenças no volume de receita.
    """)

st.markdown("---")

st.header("🎯 Conclusão")

st.markdown("""
A análise mostrou que a queda de receita em 2020 esteve principalmente
associada à redução do volume de pedidos, enquanto o ticket médio
permaneceu praticamente estável.

Também foi possível identificar a importância dos clientes recorrentes,
a concentração da receita por categorias e mercados e diferenças de
rentabilidade entre os produtos.

Esse projeto reforçou a importância de analisar os dados além dos
gráficos, buscando entender o contexto e os fatores por trás dos
resultados encontrados.
""")

st.markdown("---")

st.header("🔗 Projeto")

st.markdown("""
Confira o código, as análises e toda a estrutura do projeto no GitHub.
""")

st.markdown(
    "👉 [**Acessar projeto no GitHub**](https://github.com/Pedrohdedeus/sales-analytics)"
)