import fitz  # PyMuPDF
import re
import json
from tqdm import tqdm


def extract_dictionary_entries(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    entries = []
    current_entry = None
    current_content = []
    
    sub_terms_def = []
    sub_terms = []
    subterm = None
    
    # Process each page
    for page_num in tqdm(range(len(doc)), desc="Processing Pages"):
        page = doc[page_num]
        
        # Extract text with information about formatting
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        color = span["color"]
                        bbox = span["bbox"]
                        
                        # Terms are bold and positioned at x < 100
                        if bbox[0] < 100 and (font == 'Times New Roman,Bold' or font == 'Times New Roman,BoldItalic' or font == 'TimesNewRoman,Bold') and text.strip():
                            # If we already have an entry being processed, save it
                            if current_entry:

                                if subterm:
                                    if subterm[-2:].strip() in ['1.', '1']:
                                        sub_terms.append({
                                            "sub_term": subterm[:-2].strip(),
                                            "definitions": subterm[-2:].strip() + " " + "".join(sub_terms_def).strip()
                                        })
                                    else:
                                        sub_terms.append({
                                            "sub_term": subterm,
                                            "definitions": "".join(sub_terms_def).strip()
                                        })

                                
                                if current_entry[-2:].strip() in ['1.', '1']:
                                    # print(current_entry)
                                    entries.append({
                                        "term": current_entry[:-2].strip(),
                                        "content": current_entry[-2:].strip() + " " + "".join(current_content).strip(),
                                        "sub_terms": sub_terms
                                    })
                                else:
                                    entries.append({
                                        "term": current_entry,
                                        "content": "".join(current_content).strip(),
                                        "sub_terms": sub_terms
                                    })
                                    
                            
                            # Start a new entry
                            current_entry = text.strip()
                            subterm = None
                            current_content = []
                            sub_terms = []
                        else:
                            # Add to current entry's content
                            if current_entry:
                                if bbox[0] > 126 and bbox[0] < 127 and font == 'Times New Roman,Bold' and text.strip():
                                    if subterm:
                                        if subterm[-2:].strip() in ['1.', '1']:
                                            sub_terms.append({
                                                "sub_term": subterm[:-2].strip(),
                                                "definitions": subterm[-2:].strip() + " " + "".join(sub_terms_def).strip()
                                            })
                                        else:
                                            sub_terms.append({
                                                "sub_term": subterm,
                                                "definitions": "".join(sub_terms_def).strip()
                                            })
                                    subterm = text.strip()
                                    sub_terms_def = []

                                elif subterm:
                                    sub_terms_def.append(text + " ")
                                else:
                                    current_content.append(text + " ")
                            
    
    # Add the last entry
    if current_entry:
        entries.append({
            "term": current_entry,
            "content": "".join(current_content).strip(),
            "sub_terms": sub_terms
        })
    
    # Process each entry with regex to extract more structured information
    structured_entries = []
    for entry in entries:
        try:
            processed_entry = process_entry_content(entry["term"], entry["content"], entry["sub_terms"])
            structured_entries.append(processed_entry)
        except Exception as e:
            print(f"Error processing entry: {entry['term']}")
            print(str(e))
    
    return structured_entries


def process_entry_content(term, content, sub_terms):
    # Extract origin marker if present
    origin_pattern = r"\b(?:Ar|Id|Jw|Jk|Pk|Pr|Tr|Kl|Kd|C|IB|Pt|Mn|Br|Sl|BP|Prb|Latin|Sanskrit|Bio|Kim|Ubat|Geog|Psi|Eko)\b|\((?:Bio|Kim|Ubat|Geog|Psi|Eko|Prb|Latin|Sanskrit)\)"

    origin_match = re.match(origin_pattern, content)
    origin = origin_match.group(0) if origin_match else None
    
    # Remove origin from content if found
    if origin:
        content = re.sub(origin_pattern, '', content, 1)
    
    # Extract definitions
    definitions = []
    numbered_defs = re.findall(r'(\d+)\.\s+(.*?)(?=\s+\d+\.|$)~*;*', content, re.DOTALL)
    
    if numbered_defs:
        def_nums = []
        for def_text in numbered_defs:
            sense = def_text[0].strip()
            
            def_content = def_text[1].strip()

            if sense not in def_nums:
                def_nums.append(sense)
                definitions.append({
                    "sense": sense,
                    "definition": def_content
                })
    else:
        # Single definition
        definitions.append({
            "sense": "1",
            "definition": content.strip()
        })
    
   
    term_parts = re.match(r'([a-zA-Z\-]+)(?:\s+([IVX]+))?(?:;)?(?:\s+=\s+([a-zA-Z\-]+(?:-[a-zA-Z]+)*))?', term)
    
    base_term = term_parts.group(1) if term_parts else term
    roman_numeral = term_parts.group(2) if term_parts and term_parts.group(2) else None
    equals_part = term_parts.group(3) if term_parts and term_parts.group(3) else None
    
    # Build the structured entry
    structured_entry = {
        "term": base_term
    }
    
    if roman_numeral:
        structured_entry["roman_numeral"] = roman_numeral
        
    if equals_part:
        structured_entry["equals"] = equals_part
        
    if origin:
        structured_entry["origin"] = origin
        
    structured_entry["definitions"] = definitions

    if sub_terms:
        for sub_term in sub_terms:
            definition = sub_term['definitions']
            definitions = []
            numbered_defs = re.findall(r'(\d+)\.\s+(.*?)(?=\s+\d+\.|$)~*;*', definition, re.DOTALL)
            
            if numbered_defs:
                def_nums = []
                for def_text in numbered_defs:
                    sense = def_text[0].strip()
                    
                    def_content = def_text[1].strip()

                    if sense not in def_nums:
                        def_nums.append(sense)
                        definitions.append({
                            "sense": sense,
                            "definition": def_content
                        })
            else:
                # Single definition
                definitions.append({
                    "sense": "1",
                    "definition": definition.strip()
                })
            
            sub_term['definitions'] = definitions

        structured_entry["sub_terms"] = sub_terms
        
    return structured_entry



entries = extract_dictionary_entries('dictionary_pdf\\Kamus_Dewan_Bahasa_Edisi_Keempat_pdf.pdf')

file_path = 'output/dictionary_terms.json'
# Save the extracted entries to a JSON file
with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(entries, json_file, ensure_ascii=False, indent=4)

print(f"Dictionary entries have been saved to {file_path}")