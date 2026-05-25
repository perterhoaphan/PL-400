import docx
import json
import pandas as pd

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("--- DOCX CONTENT ---\n")
    doc = docx.Document('Question&Answer.docx')
    for i, para in enumerate(doc.paragraphs[:50]):
        if para.text.strip():
            f.write(para.text + "\n")
    
    f.write("\n--- XLSX CONTENT ---\n")
    try:
        df = pd.read_excel('Pl-400.xlsx')
        f.write(df.head(20).to_string() + "\n")
    except Exception as e:
        f.write(f"XLSX Error: {e}\n")
