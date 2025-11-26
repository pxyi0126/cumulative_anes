"""
Functions for extracting text from PDFs into .txt files.
"""
#%%
from pypdf import PdfReader
import glob
import os

def pdf_extract(file_path):
    reader = PdfReader(file_path)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_filepath = f"data/raw/txt/{base_name}_codebook.txt"
    out_path = os.path.join(os.path.dirname(new_filepath), f"{base_name}.txt")

    with open(out_path, "w", encoding="utf-8") as text_file:
        text_file.write(all_text)

    print(f"Saved: {out_path}")

# Process all PDFs (this was before I added more years, so just for 2012-2024)
# files = glob.glob("data/pdf_data/*.pdf", recursive=True)
# for file in files:
#     pdf_extract(file)

#for later cumulative data years
years = ["1952", "1960", "1994"]
for year in years:
    file_path = f"data/raw/pdf/{year}_codebook.pdf"
    pdf_extract(file_path)
