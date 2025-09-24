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
var_pattern = re.compile(r"(V24\d+[a-d,z]*)(.*)$")
rows = []

def parse_24(lines, start_idx):
    line = lines[start_idx].strip()
    match = var_pattern.match(line)
    if not match:
        return start_idx + 1
    var_name = match.group(1).strip()
    summary = match.group(2).strip()

    question, survey_q, universe, note = "", "", "", ""
    missing_label, valid_label = "", ""
    i = start_idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if var_pattern.match(line) or line.startswith("WEIGHTING VARIABLES"):
            break
        if line.startswith("Value Labels"):
            i += 1
            while line < len(lines) and re.match(r"^-?\d+\..*", line.strip()):
                label_line = lines[i].strip()
                if re.match(r"^\-\d+\..*$", label_line):
                    missing_label += label_line + "\n"
                else:
                    valid_label += label_line + "\n"
                i+=1
            continue

        if line.startswith("Question"):
            question += " " + line.replace("Question", "").strip()
        elif line.startswith("Survey Question"):
            survey_qs += " " + line.replace("Survey Question(s)", "").strip()
        elif line.startswith("Universe"):
            universe += " " + line.replace("Universe", "").strip()
        elif line.startswith("Note"):
            note += " " + line.replace("Note", "").strip()
        else:
            summary += " " + line.strip()

        i += 1

    rows.append((
        var_name,
        summary.strip(),
        question.strip(),
        survey_qs.strip(),
        universe.strip(),
        note.strip(),
        missing_label.strip(),
        valid_label.strip()
    ))
    return i



with open("data/pdf_data/2024_codebook.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
# weighting variables
weighting_vars = []

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("WEIGHTING VARIABLES"):
        i += 1

# %%