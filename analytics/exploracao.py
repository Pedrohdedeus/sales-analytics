# %%
import pandas as pd

# %%

data_dictionary = pd.read_csv("../data/dados_brutos/Data_Dictionary.csv")

data_dictionary.head()

# %%

print("Linhas: ", data_dictionary.shape[0])
print("Colunas: ", data_dictionary.shape[1])

# %%
data_dictionary

# %%
customers = pd.read_csv("../data/dados_brutos/Customers.csv",
                        encoding='latin1')

# %%
exchange_rates = pd.read_csv("../data/dados_brutos/Exchange_Rates.csv")
products = pd.read_csv("../data/dados_brutos/Products.csv")
sales = pd.read_csv("../data/dados_brutos/Sales.csv")
stores = pd.read_csv("../data/dados_brutos/Stores.csv")

# %%

print("Sales:", sales.shape)
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Stores:", stores.shape)
print("Exchange Rates:", exchange_rates.shape)

# %%

print("SALES")
print(sales.columns.tolist())

print("\nCUSTOMERS")
print(customers.columns.tolist())

print("\nPRODUCTS")
print(products.columns.tolist())

print("\nSTORES")
print(stores.columns.tolist())

print("\nEXCHANGE RATES")
print(exchange_rates.columns.tolist())

# %%

display(sales.head())
display(customers.head())
display(products.head())
display(stores.head())
display(exchange_rates.head())

# %%
print("Customers - CustomerKey únicos:", customers["CustomerKey"].nunique())
print("Customers - linhas:", len(customers))

print("Products - ProductKey únicos:", products["ProductKey"].nunique())
print("Products - linhas:", len(products))

print("Stores - StoreKey únicos:", stores["StoreKey"].nunique())
print("Stores - linhas:", len(stores))

# %%

# %%
clientes_vendas = sales["CustomerKey"].isin(customers["CustomerKey"])

produtos_vendas = sales["ProductKey"].isin(products["ProductKey"])

lojas_vendas = sales["StoreKey"].isin(stores["StoreKey"])

print("CustomerKey sem correspondência:", (~clientes_vendas).sum())
print("ProductKey sem correspondência:", (~produtos_vendas).sum())
print("StoreKey sem correspondência:", (~lojas_vendas).sum())

# %%
print(sales.dtypes)

# %%
print("SALES")
print(sales.dtypes)

print("CUSTOMERS")
print(customers.dtypes)

print("PRODUCTS")
print(products.dtypes)

print("STORES")
print(stores.dtypes)

print("EXCHANGE RATES")
print(exchange_rates.dtypes)
# %%

print("SALES")
print(sales.info())

print("CUSTOMERS")
print(customers.info())

print("PRODUCTS")
print(products.info())

print("STORES")
print(stores.info())

print("EXCHANGE RATES")
print(exchange_rates.info())

# %%

print(products.isna().sum())
print(products["Unit Price USD"].head().tolist())
print(products["Unit Cost USD"].head().tolist())
# %%
print(products["Unit Price USD"].head().max())
print(products["Unit Cost USD"].head().max())
# %%

products["Unit Price USD"] = products["Unit Price USD"].str.replace("$","",regex=False).str.replace(",","").astype(float)
products["Unit Cost USD"] = products["Unit Cost USD"].str.replace("$","",regex=False).str.replace(",","").astype(float)

# %%

products.dtypes

# %%

sales

# %%

sales["Delivery Date"] = pd.to_datetime(sales["Delivery Date"], format="%m/%d/%Y", errors="coerce")
sales.dtypes

# %%

customers["Birthday"] = pd.to_datetime(customers["Birthday"], format="%m/%d/%Y", errors="coerce")
stores["Open Date"] = pd.to_datetime(stores["Open Date"], format="%m/%d/%Y", errors="coerce")
exchange_rates["Date"] = pd.to_datetime(exchange_rates["Date"], format="%m/%d/%Y", errors="coerce")

# %%

print("Total de vendas:", len(sales))
print("Delivery Date nulos:", sales["Delivery Date"].isna().sum())
# %%

percentual_nulos = (
    sales["Delivery Date"].isna().sum()
    / len(sales)
    * 100
)

print(f"Percentual de Delivery Date nulos: {percentual_nulos:.2f}%")

# %%

delivery_nulos = sales[sales["Delivery Date"].isna()]

print(delivery_nulos["StoreKey"].value_counts().head(20))

# %%
print(delivery_nulos[["Order Number", "Order Date", "Delivery Date", "StoreKey"]].head(20))

# %%

stores.sort_values("StoreKey").head(10)

# %%

# %%
online = sales[sales["StoreKey"] == 0]
loja_fisica = sales[sales["StoreKey"] != 0]

print("ONLINE")
print("Total:", len(online))
print("Delivery nulos:", online["Delivery Date"].isna().sum())
print("Delivery preenchidos:", online["Delivery Date"].notna().sum())

print("\nLOJA FÍSICA")
print("Total:", len(loja_fisica))
print("Delivery nulos:", loja_fisica["Delivery Date"].isna().sum())
print("Delivery preenchidos:", loja_fisica["Delivery Date"].notna().sum())

# %%

# %%
print("=== SALES ===")
print(sales.isna().sum())

print("\n=== CUSTOMERS ===")
print(customers.isna().sum())

print("\n=== PRODUCTS ===")
print(products.isna().sum())

print("\n=== STORES ===")
print(stores.isna().sum())

print("\n=== EXCHANGE RATES ===")
print(exchange_rates.isna().sum())

# %%

# %%
customers_state_nulos = customers[
    customers["State Code"].isna()
]

display(customers_state_nulos)

# %%

# %%
clientes_italia = customers[
    customers["Country"] == "Italy"
]

display(
    clientes_italia[
        ["City", "State Code", "State", "Country"]
    ]
)

# %%

print("SALES:", sales.duplicated().sum())
print("CUSTOMERS:", customers.duplicated().sum())
print("PRODUCTS:", products.duplicated().sum())
print("STORES:", stores.duplicated().sum())
print("EXCHANGE RATES:", exchange_rates.duplicated().sum())
# %%

# %%
sales["Order Number"].nunique()
len(sales)
# %%

sales.duplicated(
    subset=["Order Number", "Line Item"]
).sum()

# %%

# %%
print(sales["Quantity"].describe())

# %%
print("UNIT COST")
print(products["Unit Cost USD"].describe())

print("\nUNIT PRICE")
print(products["Unit Price USD"].describe())

# %%

preco_abaixo_custo = products[
    products["Unit Price USD"] < products["Unit Cost USD"]
]

print("Produtos com preço menor que o custo:", len(preco_abaixo_custo))

# %%

preco_igual_custo = products[
    products["Unit Price USD"] == products["Unit Cost USD"]
]

print("Produtos com preço igual ao custo:", len(preco_igual_custo))
# %%

sales[["Order Date", "Delivery Date"]].dtypes
# %%
sales["Order Date"] = pd.to_datetime(sales["Order Date"], errors="coerce")

# %%
print(sales["Order Date"].dtype)
print("Datas nulas:", sales["Order Number"].isna().sum())
# %%
stores["Open Date"] = pd.to_datetime(stores["Open Date"], errors="coerce")

# %%
print(stores["Open Date"].dtype)
print("Datas nulas:", stores["Open Date"].isna().sum())

# %%

customers["Birthday"] = pd.to_datetime(customers["Birthday"], errors="coerce")

#%%

print(customers["Birthday"].dtype)
print("Datas nulas:", customers["Birthday"].isna().sum())

# %%

exchange_rates["Date"] = pd.to_datetime(exchange_rates["Date"], errors="coerce")

#%%

print(exchange_rates["Date"].dtype)
print("Datas nulas:", exchange_rates["Date"].isna().sum())

# %%
print(products["Unit Cost USD"].head())
print(products["Unit Price USD"].head())

# %%
print(sales["Currency Code"].value_counts())

# %%

exchange_rates.head()

# %%

exchange_rates["Currency"].value_counts()

# %%

duplicados_cambio = exchange_rates.duplicated(
    subset=["Date", "Currency"]
).sum()

print("Duplicidades de data + moeda:", duplicados_cambio)