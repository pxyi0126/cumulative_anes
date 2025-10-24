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
    var_pattern = re.compile(r"^(V\d+)([a-zA-Z])\-([a-zA-Z])$")
    var_str = var_string.strip()
    match = var_pattern.match(var_str)
    if not match:
        print(f"No match for: {var_str}")
        return [var_str]
    base_var, start_letter, rng_end = match.groups()

    if start_letter and rng_end.isalpha():
        start_idx = string.ascii_lowercase.index(start_letter.lower())
        end_idx = string.ascii_lowercase.index(rng_end)
        return [f"{base_var}{ch}" for ch in string.ascii_lowercase[start_idx:end_idx + 1]]
    else:
        return [var_str]

print(range_helper("V242100a-k"))

rows = []
for index, row in df_cum.iterrows():
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
        raw_vars = [v.strip() for v in str(var_2024).split(";") if v.strip()]
        expanded_vars = []

        for v in raw_vars:
            if '-' in v:
                expanded = range_helper(v)
                expanded_vars.extend(expanded)
            else:
                expanded_vars.append(v)

        var_2024_list = expanded_vars

        for v24 in var_2024_list:
            row24 = df24[df24['var_name'].str.strip() == v24]
            if row24.empty:
                print(f"Variable {v24} not found in 2024 codebook.")
                sum1 += v24 + 'does not exist in 2024 codebook\n'
                q_1 += v24 + 'does not exist in 2024 codebook\n'
                Valid1 += v24 + 'does not exist in 2024 codebook\n'
                Missing1 += v24 + 'does not exist in 2024 codebook\n'
                continue

            sum1 += row24['summary'].iloc[0] + '\n'
            q_1 += row24['question'].iloc[0] + '\n'

            if pd.notna(row24['valid_labels'].iloc[0]):
                Valid1 += row24['valid_labels'].iloc[0] + '\n'
            else:
                Valid1 += v24 + '\n'
            if pd.notna(row24['missing_labels'].iloc[0]):
                Missing1 += row24['missing_labels'].iloc[0] + '\n'
            else:
                Missing1 += '\n'
        Sources += f"2024: {var_2024}\n"

    if pd.notna(var_2020):
        raw_vars = [v.strip() for v in str(var_2020).split(";") if v.strip()]
        print("Raw vars:", raw_vars)
        expanded_vars = []
        for v in raw_vars:
            if '-' in v:
                expanded = range_helper(v)
                expanded_vars.extend(expanded)
                print(expanded_vars)
            else:
                expanded_vars.append(v)

        var_2020_list = expanded_vars

        for v20 in var_2020_list:
            row20 = df20[df20['var_name'].str.strip() == v20]
            sum2 += row20['summary'].iloc[0] + '\n'
            q_2 += row20['question'].iloc[0] + '\n'
            if pd.notna(row20['valid_labels'].iloc[0]):
                Valid2 += row20['valid_labels'].iloc[0] + '\n'
            else:
                Valid2 += '\n'
            if pd.notna(row20['missing_labels'].iloc[0]):
                Missing2 += row20['missing_labels'].iloc[0] + '\n'
            else:
                Missing2 += '\n'
        Sources += f"2020: {var_2020}\n"

    if pd.notna(var_2016):
        raw_vars = [v.strip() for v in str(var_2016).split(";") if v.strip()]
        print("Raw vars:", raw_vars)
        expanded_vars = []
        for v in raw_vars:
            if '-' in v:
                expanded = range_helper(v)
                expanded_vars.extend(expanded)
                print(expanded_vars)
            else:
                expanded_vars.append(v)

        var_2016_list = expanded_vars

        for v16 in var_2016_list:
            row16 = df16[df16['var_name'].str.strip() == v16]
            if sum2:
                sum3 += row16['description'].iloc[0] + '\n'
                # q_3 += row16['question'].iloc[0] + '\n'
                Valid3 += row16['valid_labels'].iloc[0] + '\n'
                Missing3 += row16['missing_labels'].iloc[0] + '\n'
            else:
                sum2 += row16['summary'].iloc[0] + '\n'
                q_2 += row16['question'].iloc[0] + '\n'
                Valid2 += row16['valid_labels'].iloc[0] + '\n'
                Missing2 += row16['missing_labels'].iloc[0] + '\n'
        Sources += f"2016:{var_2016}\n"

    if pd.notna(var_2012):
        # if ";" in var_2012:
        #     var_2012_list = [v12.strip() for v12 in var_2012.split(";")]
        # else:
        #     var_2012_list = [var_2012.strip()]
        # for v12 in var_2012_list:
        #     row12 = df12[df12['var_name'].str.strip() == v12]
        #     if sum2:
        #         sum3 += row12['summary'].iloc[0] + '\n'
        #         q_3 += row12['question'].iloc[0] + '\n'
        #         Valid3 += row12['valid_labels'].iloc[0] + '\n'
        #         Missing3 += row12['missing_labels'].iloc[0] + '\n'
        #     else:
        #         sum2 += row12['summary'].iloc[0] + '\n'
        #         q_2 += row12['question'].iloc[0] + '\n'
        #         Valid2 += row12['valid_labels'].iloc[0] + '\n'
        #         Missing2 += row12['missing_labels'].iloc[0] + '\n'
        Sources += f"2012:{var_2012}\n"

    if pd.notna(var_2008):
        Sources += f"2008:{var_2008}\n"

    if pd.notna(var_1992):
        Sources += f"1992:{var_1992}\n"
    if pd.notna(var_1984):
        Sources += f"1984:{var_1984}\n"
    if pd.notna(var_1968):
        Sources += f"1968:{var_1968}\n"

    rows.append({
        'Variable': curr_var,
        'sum1': sum1.strip(),
        'sum2': sum2.strip(),
        'sum3': sum3.strip(),
        'q_orig': q_orig.strip(),
        'q_1': q_1.strip(),
        'q_2': q_2.strip(),
        'q_3': q_3.strip(),
        'Valid1': Valid1.strip(),
        'Valid2': Valid2.strip(),
        'Valid3': Valid3.strip(),
        'Missing1': Missing1.strip(),
        'Missing2': Missing2.strip(),
        'Missing3': Missing3.strip(),
        'Sources': Sources.strip()
    })

df_cdf = pd.DataFrame(rows)


# df_cdf = pd.DataFrame(columns=['Variable', 'sum1','sum2', 'sum3',
#                                'q_orig', 'q_1', 'q_2', 'q_3', 'Valid1', 'Valid2',
#                                'Valid3', 'Missing1', 'Missing2', 'Missing3','Sources'])

df_cdf.to_csv("/Users/yipho/anes/cumulative_anes/test/cdf_tester.csv", index=False)

# %%
