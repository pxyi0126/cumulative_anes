# different regex for 2016
# one for strictly numerical listings
# another for the variable listings
# lastly one fo the questions
# populate three lists?
# %%
import re
import pandas as pd

var_list = []
sum_list = []
cntr_list = []
# %%
with open("2016_vars.txt", "r") as f:
    for line in f:
        cntr_pattern= r'^(\d+)'
        var_pattern = r'^V(\d+)'
        if re.match(cntr_pattern, line) and '2016' not in line:
            cntr_list.append(line.strip())
        elif re.match(var_pattern, line):
            var_list.append(line.strip())
        else:
            sum_list.append(line.strip())
# %%
with open("testing_cntr.txt", "w") as out_f:
    out_f.writelines(cntr_list)
with open("testing_var.txt", "w") as out_f:
    out_f.writelines(var_list)
with open("testing_sum.txt", "w") as out_f:
    out_f.writelines(sum_list)
# %%
df2016 = pd.DataFrame(list(zip(cntr_list, var_list, sum_list)),
                      columns = ['index', 'variable', 'question'])
# %%
df2016
# %%
csv2016 = df2016.to_csv("anes_2016_vars.csv", index=False)
csv2016
# %%
# convert csv to xlsx
read_file = pd.read_csv("anes_2016_vars.csv")
read_file.to_excel("anes_2016_vars.xlsx", index=None, header=True)
# %%
