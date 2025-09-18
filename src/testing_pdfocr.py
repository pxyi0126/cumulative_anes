from pypdf import PdfReader

# Specify the path to your PDF file
pdf_file_path = "2024_codebook.pdf"

# Create a PdfReader object
reader = PdfReader(pdf_file_path)

# Get the number of pages in the PDF
num_pages = len(reader.pages)
print(f"Number of pages: {num_pages}")

# Extract text from a specific page (e.g., the first page)
first_page = reader.pages[0]
page_text = first_page.extract_text()
print("\nText from the first page:")
print(page_text)

# You can iterate through all pages to extract all text
all_text = ""
for page_num in range(num_pages):
    page = reader.pages[page_num]
    all_text += page.extract_text() + "\n"  # Add newline for readability between pages

#write all of this into a separate file
with open("2024_codebook.txt", "w") as text_file:
    text_file.write(all_text)