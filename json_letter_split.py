import json
import os

with open('output/dictionary_terms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ensure the output directory exists
output_dir = 'output/split_by_letter'
os.makedirs(output_dir, exist_ok=True)

print("Terms: ",len(data))


# Create a dictionary to group terms by their first letter
grouped_data = {}
for term in data:
    first_letter = term['term'][0].lower()  # Get the first letter and convert to lowercase
    if first_letter.isalpha():  # Ensure it's a valid alphabet character
        grouped_data.setdefault(first_letter, []).append(term)

# Write each group to a separate JSON file
for letter, terms in grouped_data.items():
    file_path = os.path.join(output_dir, f"{letter}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=4)

print(f"JSON files have been split and saved in '{output_dir}'")