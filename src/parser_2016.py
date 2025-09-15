# %%
import re
import pandas as pd
import os

os.chdir("/Users/yipho/anes/cumulative_anes/data")

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
print(cntr_list)
print(len(cntr_list)) #1839
filter_cntr = [x for x in cntr_list if x != '']
print(len(filter_cntr)) #1841

print(var_list)
print(len(var_list)) #1841
filter_var = [x for x in var_list if x != '']
print(len(filter_var)) #1841

print(sum_list)
print(len(sum_list)) #1964
filter_sum = [x for x in sum_list if x != '']
print(len(filter_sum)) #1842...??
print(filter_sum[-3:])
# %%
df2016 = pd.DataFrame(list(zip(filter_cntr, filter_var, filter_sum)),
                      columns = ['index', 'variable', 'question'])
# %%

csv2016 = df2016.to_csv("parsed_2016.csv", index=False)
csv2016
# %%
# convert csv to xlsx
read_file = pd.read_csv("parsed_2016.csv")
read_file.to_excel("parsed_2016.xlsx", index=None, header=True)
# %%
