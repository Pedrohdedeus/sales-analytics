# %%
import pandas as pd

# %%

customers = pd.read_csv("../data/dados_brutos/Customers.csv",
                        encoding='latin1')
exchange_rates = pd.read_csv("../data/dados_brutos/Exchange_Rates.csv")
products = pd.read_csv("../data/dados_brutos/Products.csv")
sales = pd.read_csv("../data/dados_brutos/Sales.csv")
stores = pd.read_csv("../data/dados_brutos/Stores.csv")
