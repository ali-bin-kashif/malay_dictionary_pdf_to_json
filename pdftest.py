import fitz  # PyMuPDF
import re
import json
from tqdm import tqdm

# Open your PDF
doc = fitz.open("dictionary_pdf\Kamus_Dewan_Bahasa_Edisi_Keempat_pdf.pdf")

for page_number, page in enumerate(doc, start=1):
    # print(page.get_text("dict")["blocks"])

        # print(page)
    
    if page_number >= 793 and page_number < 795:
        blocks = page.get_text("dict")["blocks"] 
        # text = repr(page.get_text())  # Get raw string with escape sequences
        # print(text)

        for block in blocks:
            if block["type"] == 0:  # text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        color = span["color"]
                        bbox = span["bbox"]
                        print(f"Page {page_number} | Text: {text} | Font: {font} | Size: {size} | Color: {color} | BBox: {bbox}")
                        # if bbox[0] < 100 and font == 'Times New Roman,Bold' and text.strip() != '':
                        #     print(f"Page {page_number} | Text: {text} | Font: {font} | Size: {size} | Color: {color} | BBox: {bbox}")
                        # if bbox[0] > 126 and bbox[0] < 127 and font == 'Times New Roman,Bold' and text.strip():
                        #     print(f"Page {page_number} | Text: {text} | Font: {font} | Size: {size} | Color: {color} | BBox: {bbox}")
                        
    
    # if page_number > 3:
    #     break
    
    
    
# # Pattern to match dictionary entries
# pattern = r'(?:^|\n)([a-zA-Z\-]+(?:\s+[IVX]+)?(?:;)?(?:\s+=\s+[a-zA-Z\-]+(?:-[a-zA-Z]+)*)?)\s+(?:([A-Za-z]+)\s+)?((?:(?:\d+\.\s+.+?(?=\d+\.|;|\n(?=[a-zA-Z\-]+(?:\s+[IVX]+)?(?:;)?(?:\s+=\s+)?\s+(?:[A-Za-z]+\s+)?)|$))|.+?)(?=\n(?=[a-zA-Z\-]+(?:\s+[IVX]+)?(?:;)?(?:\s+=\s+)?\s+(?:[A-Za-z]+\s+)?)|$))'



# for page_number, page in enumerate(doc, start=1):
#     text = page.get_text()
#     matches = re.finditer(pattern, text, re.DOTALL)

#     for match in matches:
#         term = match.group(1).strip()
#         origin = match.group(2).strip() if match.group(2) else None
#         definition_text = match.group(3).strip()

#         print(f"Term: {term}, Origin: {origin}, Definition: {definition_text}")
#         print('\n\n============\n\n')


    # if page_number > 5:
    #     break
    
# # Open the PDF
# doc = fitz.open("Kamus_Dewan_Bahasa_Edisi_Keempat_pdf.pdf")

# entries = []

# # Regular expressions for parsing
# main_entry_re = re.compile(r"^(.*?)\s+(?:([A-Z][a-z]{0,3})\s+)?(?:I{0,3}|II|III|IV)?\s*(?:\d+\.)?")

# # definition_re = re.compile(r"(\d+)\.\s*(.*)")
# # subentry_re = re.compile(r"^\s*(\w+)\s+(\d+)\.\s*(.*)")

# current_entry = None

# pattern = r'([a-zA-Z\-]+(?:\s+[IVX]+)?)(?:\s+([A-Za-z]+))?\s+((?:(?:\d+\.\s+.+?(?=\d+\.|;|\n\w|$))|.+?)(?=\n[a-zA-Z\-]+(?:\s+[IVX]+)?\s+|$))'

# for page in tqdm(doc, desc="Processing Pages"):
#     text = page.get_text()
#     # lines = text.split('\n')

#     matches = re.finditer(pattern, text, re.DOTALL)

#     for match in matches:
#         term = match.group(1).strip()
#         origin = match.group(2).strip() if match.group(2) else None
#         definition_text = match.group(3).strip()

#         print(f"Term: {term}, Origin: {origin}, Definition: {definition_text}")
#         print('\n\n============\n\n')


