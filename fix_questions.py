import json
import re

try:
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    count = 0
    for q in questions:
        if 'question' in q and '[Variation' in q['question']:
            q['question'] = re.sub(r'\[Variation \d+\]\s*', '', q['question'])
            count += 1
            
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
        
    print(f"Fixed {count} questions.")
except Exception as e:
    print(f"Error: {e}")
