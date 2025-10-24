# Last variable used: VCF9282
# everything after should be VCF9282 + i
import pandas as pd
import re
import string

# read in the data and rename the column for 2024
df_cum = pd.read_csv("/Users/yipho/anes/cumulative_anes/test/3x_test.csv")
df_cum.rename(columns={'2024 variables used 2x previous': '2024'}, inplace=True)

df24 = pd.read_csv("/Users/yipho/anes/cumulative_anes/data/pdf_data/2024_pcodebook.csv")
df20 = pd.read_csv("/Users/yipho/anes/cumulative_anes/data/pdf_data/2020_pcodebook.csv")
df16 = pd.read_csv("/Users/yipho/anes/cumulative_anes/data/pdf_data/2016_pcodebook.csv")
df12 = pd.read_csv("/Users/yipho/anes/cumulative_anes/data/pdf_data/2012_pcodebook.csv")


def range_helper(var_string):
    var_pattern = re.compile(r"(V\d+)(\w)\-(\w)")

    var_str = var_string.strip()

    base_var = var_pattern.match(var_string).group(1)
    start_letter = var_pattern.match(var_string).group(2)
    rng_end = var_pattern.match(var_string).group(3)

    if start_letter and rng_end.isalpha():
        start_idx = string.ascii_lowercase.index(start_letter.lower())
        end_idx = string.ascii_lowercase.index(rng_end)
        return [f"{base_var}{ch}" for ch in string.ascii_lowercase[start_idx:end_idx + 1]]
    else:
        return [var_str]

range_helper("V202114a-k")

print(df24.columns)
print(df_cum.columns)
rows = []
for index, row in df_cum.iterrows():
    # print(index)
    curr_var = f"VCF{9282+ index}"
    print(f"New CDF variable {curr_var}...")
    var_2024 = row['2024']
    var_2020 = row['2020']
    var_2016 = row['2016']
    var_2012 = row['2012']

    # Rogue Variables lol
    var_2008 = row['2008']
    var_1992 = row['1992']
    var_1984 = row['1984']
    var_1968 = row['1968']

    sum1 = ""
    sum2 = ""
    sum3 = ""
    q_orig = ""
    q_1 = ""
    q_2 = ""
    q_3 = ""
    Valid1 = ""
    Valid2 = ""
    Valid3 = ""
    Missing1 = ""
    Missing2 = ""
    Missing3 = ""
    Sources = ""
    q_orig = row["topic"]

    if pd.notna(var_2024):
        if ";" in var_2024:
            var_2024_list = [v24.strip() for v24 in var_2024.split(";")]
            # print(var_2024_list)
        else:
            var_2024_list = [var_2024.strip()]
        for v24 in var_2024_list:
            row24 = df24[df24['var_name'].str.strip() == v24]
            sum1 += row24['summary'].iloc[0]
            q_1 += row24['question'].iloc[0]
            Valid1 += row24['valid_labels'].iloc[0]
            Missing1 += row24['missing_labels'].iloc[0]
        Sources += f"2024:{var_2024}\n"

    if pd.notna(var_2020):
        if ";" in var_2020:
            var_2020_list = [v20.strip() for v20 in var_2020.split(";")]
        else:
            var_2020_list = [var_2020.strip()]
        for v20 in var_2020_list:
            row20 = df20[df20['var_name'] == v20]
        for v20 in var_2020_list:
            row20 = df20[df20['var_name'].str.strip() == v20]
            sum2 += row20['summary'].iloc[0] + '\n'
            q_2 += row20['question'].iloc[0] + '\n'
            Valid2 += row20['valid_labels'].iloc[0] + '\n'
            Missing2 += row20['missing_labels'].iloc[0] + '\n'
        Sources += f"2020:{var_2020}\n"

    if pd.notna(var_2016):
        if ";" in var_2016:
            var_2016_list = [v16.strip() for v16 in var_2016.split(";")]
        else:
            var_2016_list = [var_2016.strip()]
        for v16 in var_2016_list:
            row16 = df16[df16['var_name'].str.strip() == v16]
            if sum2:
                sum3 += row16['description'].iloc[0] + '\n'
                q_3 += row16['question'].iloc[0] + '\n'
                Valid3 += row16['valid_labels'].iloc[0] + '\n'
                Missing3 += row16['missing_labels'].iloc[0] + '\n'
            else:
                sum2 += row16['summary'].iloc[0] + '\n'
                q_2 += row16['question'].iloc[0] + '\n'
                Valid2 += row16['valid_labels'].iloc[0] + '\n'
                Missing2 += row16['missing_labels'].iloc[0] + '\n'
        Sources += f"2016:{var_2016}\n"

    if pd.notna(var_2012):
        if ";" in var_2012:
            var_2012_list = [v12.strip() for v12 in var_2012.split(";")]
        else:
            var_2012_list = [var_2012.strip()]
        for v12 in var_2012_list:
            row12 = df12[df12['var_name'].str.strip() == v12]
            if sum2:
                sum3 += row12['summary'].iloc[0] + '\n'
                q_3 += row12['question'].iloc[0] + '\n'
                Valid3 += row12['valid_labels'].iloc[0] + '\n'
                Missing3 += row12['missing_labels'].iloc[0] + '\n'
            else:
                sum2 += row12['summary'].iloc[0] + '\n'
                q_2 += row12['question'].iloc[0] + '\n'
                Valid2 += row12['valid_labels'].iloc[0] + '\n'
                Missing2 += row12['missing_labels'].iloc[0] + '\n'
        Sources += f"2012:{var_2012}\n"

    if pd.notna(var_2008):
        Sources += f"2008:{var_2008}\n"

    if pd.notna(var_1992):
        Sources += f"1992:{var_1992}\n"
    if pd.notna(var_1984):
        Sources += f"1984:{var_1984}\n"
    if pd.notna(var_1968):
        Sources += f"1968:{var_1968}\n"



df_cdf = pd.DataFrame(columns=['Variable', 'sum1','sum2', 'sum3',
                               'q_orig', 'q_1', 'q_2', 'q_3', 'Valid1', 'Valid2',
                               'Valid3', 'Missing1', 'Missing2', 'Missing3','Sources'])

df_cdf.to_csv("/Users/yipho/anes/cumulative_anes/test/cdf_tester.csv", index=False)
