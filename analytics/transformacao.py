# %%
import pandas as pd

from carregamento import sales, products, customers, exchange_rates, stores

# %%
print("Produtos diferentes nas vendas:", sales["ProductKey"].nunique())
print("Produtos cadastrados:", products["ProductKey"].nunique())
print("ProductKeys duplicadas:", products["ProductKey"].duplicated().sum())
# %%

products["Unit Cost USD"] = (
    products["Unit Cost USD"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

products["Unit Price USD"] = (
    products["Unit Price USD"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# %%

print(products["Unit Cost USD"].dtype)
print(products["Unit Price USD"].dtype)

# %%

products.head()

# %%

base_analitica = sales.merge(
                             products,
                             on="ProductKey",
                             how="left"
                             )


# %%

print("Linhas em sales: ", len(sales))
print("Linhas pós merge: ", len(base_analitica))
# %%
print("Produtos não encontrados:", base_analitica["Product Name"].isna().sum())
# %%
print("Clientes diferentes nas vendas:", sales["CustomerKey"].nunique())
print("Clientes cadastrados:", customers["CustomerKey"].nunique())
print("CustomerKeys duplicadas:", customers["CustomerKey"].duplicated().sum())

# %%

base_analitica = base_analitica.merge(

    customers,
    on="CustomerKey",
    how="left"
)
# %%
print("Linhas antes do merge:", len(sales))
print("Linhas após customers:", len(base_analitica))
# %%
print("Clientes não encontrados:", base_analitica["Name"].isna().sum())

# %%

print("Lojas diferentes nas vendas:", sales["StoreKey"].nunique())
print("Lojas cadastradas:", stores["StoreKey"].nunique())
print("StoreKeys duplicadas:", stores["StoreKey"].duplicated().sum())
# %%

base_analitica= base_analitica.merge(
    stores,
    on="StoreKey",
    how="left"
)

# %%
print("Linhas em sales:", len(sales))
print("Linhas após stores:", len(base_analitica))
print("Lojas não encontradas:", base_analitica["Country_y"].isna().sum())
# %%
print(base_analitica.columns.tolist())
# %%
base_analitica = base_analitica.rename(columns={
    "State_x": "Customer State",
    "Country_x": "Customer Country",
    "State_y": "Store State",
    "Country_y": "Store Country"
})
# %%
print(base_analitica.columns.tolist())
# %%
print("Order Date:", base_analitica["Order Date"].dtype)
print("Date:", exchange_rates["Date"].dtype)

# %%
base_analitica["Order Date"] = pd.to_datetime(
    base_analitica["Order Date"],
    format="%m/%d/%Y"
)

exchange_rates["Date"] = pd.to_datetime(
    exchange_rates["Date"],
    format="%m/%d/%Y"
)
# %%

print("Order Date:", base_analitica["Order Date"].dtype)
print("Date:", exchange_rates["Date"].dtype)

# %%

base_analitica = base_analitica.merge(
    exchange_rates,
    left_on=["Order Date", "Currency Code"],
    right_on=["Date", "Currency"],
    how="left"
)
# %%
print("Linhas antes:", len(sales))
print("Linhas depois:", len(base_analitica))
print("Câmbios não encontrados:", base_analitica["Exchange"].isna().sum())

# %%

base_analitica = base_analitica.drop(columns=["Date", "Currency"])

# %%
base_analitica.head()

# %%

base_analitica["Receita USD"] = ( base_analitica["Quantity"] * base_analitica["Unit Price USD"])

base_analitica["Custo USD"] = (base_analitica["Quantity"] * base_analitica["Unit Cost USD"])

base_analitica["Lucro USD"] = (base_analitica["Receita USD"] - base_analitica["Custo USD"])

# %%

base_analitica.head()

# %%

base_analitica.to_csv("../data/dados_processados/base_analitica.csv", index=False)