import pandas as pd

df = pd.read_csv("European_Bank.csv")

print("✅ Shape (rows, columns):", df.shape)
print("\n✅ Column Names:")
print(df.columns.tolist())
print("\n✅ First 5 rows:")
print(df.head())
print("\n✅ Data Types:")
print(df.dtypes)