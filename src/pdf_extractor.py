# %%
from pypdf import PdfReader
import glob
import os
# %%
def pdf_extract(file_path):
    # Create PdfReader object
    reader = PdfReader(file_path)

    # Extract all text
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"


    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_path = os.path.join(os.path.dirname(file_path), f"{base_name}.txt")

    with open(out_path, "w", encoding="utf-8") as text_file:
        text_file.write(all_text)

    print(f"Saved: {out_path}")

# Process all PDFs
files = glob.glob("data/pdf_data/*.pdf", recursive=True)
for file in files:
    pdf_extract(file)
# %%
# Parsing through 2024 codebook txt
import re
import pandas as pd
import os
os.chdir("/Users/yipho/anes/cumulative_anes/data/pdf_data")
var_pattern = re.compile(r"(V\d+[a-d,x,z,_orig]*)(.*)$")
rows = []

def parse_24(lines, start_idx):
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1
    var_name = match.group(1).strip()
    summary = match.group(2).strip()
    j = start_idx + 1
    while j < len(lines) and not lines[j].strip().startswith("Question") \
        and not lines[j].strip().startswith("Value Labels") \
        and not var_pattern.match(lines[j].strip()) \
        and not re.match(r"^\d*\s*CODEBOOK:.*", lines[j].strip()):
        summary += " " + lines[j].strip()
        j += 1

    question = ""
    missing_label, valid_label = "", ""
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if var_pattern.match(line) or line.startswith("WEIGHTING VARIABLES"):
            break

        if line.startswith("Question"):
            q_block = line.replace("Question", "").strip()
            if q_block:
                question += " " + q_block
            j = i+1
            while j < len(lines):
                nxt = lines[j].strip()
                if (nxt.startswith("Value Labels") or
                    var_pattern.match(nxt)):
                    break
                question += " " + nxt
                j += 1
            i = j
            continue
        if line.startswith("Value Labels"):
            rest = line.replace("Value Labels", "").strip()
            if rest and re.match(r"^-?\d+\..*", rest):
                if re.match(r"^\-\d+\..*$", rest):
                    missing_label += rest + "\n"
                else:
                    valid_label += rest + "\n"

            i += 1
            while i < len(lines) and re.match(r"^-?\d+\..*", lines[i].strip()):
                label_line = lines[i].strip()
                if re.match(r"^\-\d+\..*$", label_line):
                    missing_label += label_line + "\n"
                elif re.match(r"^\d+\..*$", label_line):
                    valid_label += label_line + "\n"
                i+=1
            continue

        i += 1
    rows.append((
        var_name,
        summary.strip(),
        question.strip(),
        missing_label.strip(),
        valid_label.strip()
    ))
    return i

with open("2024_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    if var_pattern.match(line):
        i = parse_24(lines, i)
    else:
        i += 1

df_24 = pd.DataFrame(rows, columns=[
    "var_name", "summary", "question", "missing_labels", "valid_labels"
])

df_24.to_csv("2024_pcodebook.csv", index=False)
# %%
# Parsing through 2020 codebook txt
import re
import pandas as pd
import os
os.chdir("/Users/yipho/anes/cumulative_anes/data/pdf_data")
var_pattern = re.compile(r"(V\d+[a-d,x,z,_orig]*)(.*)$")
rows = []

def parse_24(lines, start_idx):
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1
    var_name = match.group(1).strip()
    summary = match.group(2).strip()
    j = start_idx + 1
    while j < len(lines) and not lines[j].strip().startswith("Question") \
        and not lines[j].strip().startswith("Value Labels") \
        and not var_pattern.match(lines[j].strip()) \
        and not re.match(r"^\d*\s*CODEBOOK:.*", lines[j].strip()):
        summary += " " + lines[j].strip()
        j += 1

    question = ""
    missing_label, valid_label = "", ""
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if var_pattern.match(line) or line.startswith("WEIGHTING VARIABLES"):
            break

        if line.startswith("Question"):
            q_block = line.replace("Question", "").strip()
            if q_block:
                question += " " + q_block
            j = i+1
            while j < len(lines):
                nxt = lines[j].strip()
                if (nxt.startswith("Value Labels") or
                    var_pattern.match(nxt)):
                    break
                question += " " + nxt
                j += 1
            i = j
            continue
        if line.startswith("Value Labels"):
            rest = line.replace("Value Labels", "").strip()
            if rest and re.match(r"^-?\d+\..*", rest):
                if re.match(r"^\-\d+\..*$", rest):
                    missing_label += rest + "\n"
                else:
                    valid_label += rest + "\n"

            i += 1
            while i < len(lines) and re.match(r"^-?\d+\..*", lines[i].strip()):
                label_line = lines[i].strip()
                if re.match(r"^\-\d+\..*$", label_line):
                    missing_label += label_line + "\n"
                elif re.match(r"^\d+\..*$", label_line):
                    valid_label += label_line + "\n"
                i+=1
            continue

        i += 1
    rows.append((
        var_name,
        summary.strip(),
        question.strip(),
        missing_label.strip(),
        valid_label.strip()
    ))
    return i

with open("2020_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    if var_pattern.match(line):
        i = parse_24(lines, i)
    else:
        i += 1

df_20 = pd.DataFrame(rows, columns=[
    "var_name", "summary", "question", "missing_labels", "valid_labels"
])

df_20.to_csv("2020_pcodebook.csv", index=False)
# %%
# Parsing through 2016 codebook txt
import re
import pandas as pd
import os
os.chdir("/Users/yipho/anes/cumulative_anes/data/pdf_data")
var_pattern = re.compile(r"(V\d+[a-z,_orig]*)(.*)$")
val_pattern = re.compile(r"^(\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
missing_pattern = re.compile(r"(\-\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")

def parse_16(lines, start_idx, rows):
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1, rows
    varname = match.group(1).strip()
    summary = ""
    valid_label = ""
    missing_label = ""
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Label:"):
            summary = line.replace("Label:", "").strip()
        if var_pattern.match(line):
            break
        if "Percentages" in line:
            i += 3
            while i < len(lines):
                block = re.sub(r"\s+", " ", lines[i]).strip()
                if not block:
                    i += 1
                    continue

                if block.startswith("ANES") or \
                    block.startswith("Label:") or block.startswith("Item name:"):
                    break
                if block.startswith("FTF") or block.startswith("No wgt"):
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

    rows.append((varname, summary, valid_label, missing_label))
    return i, rows

rows = []
with open("2016_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
i = 0
while i < len(lines):
    i, rows = parse_16(lines, i, rows)


df_16 = pd.DataFrame(rows, columns=["var_name", "description", "valid_labels", "missing_labels"])
print(df_16.head())
df_16.to_csv("2016_pcodebook.csv", index=False)

# need to edit it so that if the variable already exists in the list, that if it is found again
# we add it to the existing entry of it

# %%
import re
import pandas as pd
import os
os.chdir("/Users/yipho/anes/cumulative_anes/test")
page_pattern = re.compile(r"^ANES.*?-page\b.*")
val_pattern = re.compile(r"^(\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")
missing_pattern = re.compile(r"(\-\d+)\.\s*([A-Za-z].*?)(?=\s+\d|\s*$)")

def parse_12(lines, start_idx, rows):
    line = lines[start_idx].strip()
    print(f"Processing line {start_idx}: {line}")
    varname = ""
    summary = ""
    valid_label = ""
    missing_label = ""
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Label:"):
            summary = line.replace("Label:", "").strip()
        if page_pattern.match(line):
            varname = lines[i+1].strip()
            break
        if "Percentages" in line:
            i += 3
            while i < len(lines):
                block = re.sub(r"\s+", " ", lines[i]).strip()
                if not block:
                    i += 1
                    continue

                if block.startswith("Label:") or block.startswith("Item name:") \
                    or page_pattern.match(block):
                    break
                if block.startswith("FTF") or block.startswith("No wgt"):
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

    rows.append((varname, summary, valid_label, missing_label))
    return i, rows

rows = []
with open("2012small.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
i = 0
while i < len(lines):
    i, rows = parse_12(lines, i, rows)


df_12 = pd.DataFrame(rows, columns=["var_name", "description", "valid_labels", "missing_labels"])
print(df_12.head())
df_12.to_csv("2012_pcodebook.csv", index=False)

# %%
