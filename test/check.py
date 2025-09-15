import difflib
import pandas as pd

df2016 = pd.read_csv("parsed_2016.csv")
df20162 = pd.read_excel("2016_var.xlsx")
df20162.to_csv("2016_var.csv", index=False)
# df20162['1'] = df20162['1'].astype(str)

col1 = df2016["variable"].astype(str).tolist()
col2 = df20162['version'].astype(str).tolist()


diff = difflib.unified_diff(col1, col2, fromfile='parsed_2016.csv', tofile="2016_var.csv")
for line in diff:
    print(line)

print(len(col1), len(col2))
