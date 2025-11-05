# Parsing through 2016 codebook txt
import re
import pandas as pd
import os

os.chdir("/Users/yipho/anes/cumulative_anes/data/pdf_data")

var_pattern = re.compile(r"(V\d+[a-z,_orig]*)(.*)$")
val_pattern = re.compile(r"^(\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
missing_pattern = re.compile(r"(\-\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")

def parse_16(lines, start_idx, rows_dict):
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1, rows_dict

    varname = match.group(1).strip()
    summary = ""
    valid_label = ""
    missing_label = ""
    question = ""
    i = start_idx + 1

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Label:"):
            summary = line.replace("Label:", "").strip()
        if line.startswith("Question:"):
            q_lines = []
            while i < len(lines) and "Unweighted F requencies" not in lines[i]:
                cleaned = lines[i].strip().replace("Question:", "").strip()
                if cleaned:
                    q_lines.append(cleaned)
                i += 1
            question = " ".join(q_lines).strip()
            continue

        if var_pattern.match(line):
            break
        if "Percentages" in line:
            i += 3
            while i < len(lines):
                block = re.sub(r"\s+", " ", lines[i]).strip()
                if not block:
                    i += 1
                    continue

                if block.startswith(("ANES", "Label:", "Item name:")):
                    break
                if block.startswith(("FTF", "No wgt")):
                    i += 1
                    continue

                val_match = val_pattern.match(block)
                missing_match = missing_pattern.match(block)

                if val_match:
                    valid_label += f"{val_match.group(1)}. {val_match.group(2).strip()}\n"
                elif missing_match:
                    missing_label += f"{missing_match.group(1)}. {missing_match.group(2).strip()}\n"
                i += 1
            continue
        i += 1

    # If variable already exists, append new info
    if varname in rows_dict:
        prev_summary, prev_q, prev_valid, prev_missing = rows_dict[varname]
        summary = (prev_summary + "\n" + summary).strip()
        question = (prev_q + "\n" + question).strip()
        valid_label = (prev_valid + valid_label).strip()
        missing_label = (prev_missing + missing_label).strip()
        rows_dict[varname] = (summary, question, valid_label, missing_label)
    else:
        rows_dict[varname] = (summary, question, valid_label, missing_label)

    return i, rows_dict

rows_dict = {}
with open("2016_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    i, rows_dict = parse_16(lines, i, rows_dict)

# Convert dict to DataFrame
df_16 = pd.DataFrame(
    [(k, v[0], v[1], v[2], v[3]) for k, v in rows_dict.items()],
    columns=["var_name", "summary", "question", "valid_labels", "missing_labels"]
)

df_16.to_csv("2016_pcodebook.csv", index=False)