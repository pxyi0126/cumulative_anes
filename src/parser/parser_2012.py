# Parsing through 2012 codebook txt
import re
import pandas as pd
import os

os.chdir("/Users/yipho/anes/cumulative_anes/data/pdf_data")
page_pattern = re.compile(r"^ANES.*?-?\s*page\s*\d+")
val_pattern = re.compile(r"^(\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
missing_pattern = re.compile(r"(\-\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
def parse_12(lines, start_idx, rows_dict):
    line0 = lines[start_idx].strip()
    print(f"Processing line {start_idx}: {line0}")
    varname = ""
    summary = ""
    valid_label = ""
    missing_label = ""
    i = start_idx + 1
    if i >= len(lines):
        return i, rows_dict
    if page_pattern.match(line0):
        if i < len(lines):
            varname = lines[i].strip()
        i += 1
    while i < len(lines):
        line = lines[i].strip()
        print(f"Processing line {i}: {line}")

        if line.startswith("Label:"):
            summary = line.replace("Label:", "").strip()

        if page_pattern.match(line):
            break

        if line.startswith("Unweighted Frequencies"):
            i += 1
            while i < len(lines):
                block = re.sub(r"\s+", " ", lines[i]).strip()
                if not block:
                    i += 1
                    continue

                if block.startswith("Label:") or block.startswith("Item name:") or page_pattern.match(block):
                    break

                val_match = val_pattern.match(block)
                missing_match = missing_pattern.match(block)

                if val_match:
                    valid_label += f"{val_match.group(1)}. {val_match.group(2).strip()}\n"
                elif missing_match:
                    missing_label += f"{missing_match.group(1)}. {missing_match.group(2).strip()}\n"
                i += 1
            break

        i += 1

    rows_dict[varname] = (summary, valid_label, missing_label)
    return i, rows_dict

rows_dict = {}

with open("2012_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
i = 0
while i < len(lines):
    i, rows_dict = parse_12(lines, i, rows_dict)

df_12 = pd.DataFrame([(k, v[0], v[1], v[2]) for k, v in rows_dict.items()],
    columns=["var_name", "description", "valid_labels", "missing_labels"])
print(df_12.head())
df_12.to_csv("2012_pcodebook.csv", index=False)