import pandas as pd

df = pd.read_csv("pokemon.csv", delimiter=",")
print(df[:10])
print(df.info())
print(df.describe())

print(df.loc[df["Speed"] > 110, ["Name", "Speed"]].sort_values("Speed", ascending=False))

grouped_result = df.loc[:, ["Type 1", "HP"]].groupby("Type 1")
print(grouped_result.mean())