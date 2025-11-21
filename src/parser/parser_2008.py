# Parsing through 2008 codebook txt
import re
import pandas as pd
import os
import shutil
os.chdir("/Users/yipho/anes/cumulative_anes/data/raw/txt")

var_pattern = re.compile(r"(V\d+[a-z,_orig]*)(.*)$")
val_pattern = re.compile(r"^(\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
# There are some codes that say Range: \d-\d for valid codes,
# for now we don't need to consider it but if we needed it later keep it in mind
missing_pattern = re.compile(r"(\-\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")

rows = []

# No need to merge the files, everything is in the pre.txt file
# perhaps for future reference:
with open('merged_08', 'wb'):
    for filename in ['2008_post.txt', '2008_pre.txt']:
        with open(filename, 'rb') as f:
            shutil.copyfileobj(f, 'merged_08')

def parse_08(lines, start_idx):
    print(f"Parsing starting at line {start_idx}")
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1, rows

    varname = match.group(1).strip()
    summary = match.group(2).strip()
    question = ""
    valid_label = ""
    missing_label = ""
    i = start_idx + 1

    divider = re.compile(r"^-{5,}$")
    # next_var = re.compile(r"^V\d+")

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("TYPE:") or line.startswith("NOTES:"):
            break

        if divider.match(line) and not question:
            block_lines = []
            i += 1

            print(f"Found question divider for {varname}")
            while i < len(lines) and not divider.match(lines[i].strip()):
                block_lines.append(lines[i].rstrip())
                i += 1
            question = "\n".join(block_lines).strip()

            if i < len(lines) and divider.match(lines[i].strip()):
                i += 1
            continue

        if "VALID CODES" in line.upper():
            print(f"Found VALID CODES for {varname}")
            i += 2
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith("MISSING CODES:") or re.match(r"^V\d+", line):
                    break
                val_match = val_pattern.match(line)
                if val_match:
                    valid_label += val_match.group() + "\n"
                i += 1
            continue

        if line.startswith("MISSING CODES:"):
            i += 2
            print(f"Found MISSING CODES for {varname}")
            while i < len(lines):
                line = lines[i].strip()
                if not line or re.match(r"^V\d+", line):
                    break
                miss_match = missing_pattern.match(line)
                if miss_match:
                    missing_label += miss_match.group() + "\n"
                i += 1
            continue
        i += 1
    rows.append((varname, summary, question, valid_label.strip(), missing_label.strip()))
    return i, rows

with open("merged_08.txt", "r", errors='replace') as f:
    lines = f.readlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    if var_pattern.match(line):
        i, rows = parse_08(lines, i)
    else:
        i += 1

df_2008 = pd.DataFrame(rows, columns=['var_name', 'summary', 'question', 'valid_labels', 'missing_labels'])
df_2008.to_csv("2008_pcodebook.csv", index=False, encoding="utf-8")







