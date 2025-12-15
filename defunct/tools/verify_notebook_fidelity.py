
import json
import argparse
import re
import sys
from pathlib import Path

def normalize_text(text):
    """
    Normalize text for comparison:
    - Lowercase
    - Remove markdown formatting keys (*, #, -, >, `)
    - Collapse whitespace
    """
    # Remove markdown characters
    text = re.sub(r'[\*\#\-\>\`]', ' ', text)
    # Remove image references like ![...](...)
    text = re.sub(r'\!\[.*?\]\(.*?\)', '', text)
    # Lowercase
    text = text.lower()
    # Collapse whitespace (newlines, tabs, multiple spaces become single space)
    text = ' '.join(text.split())
    return text

def get_notebook_text(ipynb_path):
    """Extract all text from markdown cells in the notebook."""
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Error reading notebook: {e}")
        sys.exit(1)
        
    text_content = []
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'markdown':
            # join list of lines into a single string
            cell_text = ''.join(cell['source'])
            text_content.append(cell_text)
            
    return "\n".join(text_content)

def get_source_text(md_path):
    """Read the source markdown file."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading source markdown: {e}")
        sys.exit(1)

def verify_fidelity(source_path, notebook_path):
    print(f"Checking fidelity...")
    print(f"Source:   {source_path}")
    print(f"Notebook: {notebook_path}")
    
    source_raw = get_source_text(source_path)
    nb_raw = get_notebook_text(notebook_path)
    
    # We want to check if the STRUCTURE and CONTENT of source is in notebook.
    # Approach: Split source into "paragraphs" (double newlines) and verify each paragraph exists in the notebook.
    
    # Split by double newline to get paragraphs/sections
    source_chunks = re.split(r'\n\s*\n', source_raw)
    
    # Normalize the entire notebook content for searching
    nb_norm = normalize_text(nb_raw)
    
    missing_chunks = []
    matched_count = 0
    
    for chunk in source_chunks:
        if not chunk.strip():
            continue
            
        # headers or images might need special handling, but let's try text matching
        chunk_norm = normalize_text(chunk)
        
        # If chunk is too short (like "Part 1"), it might be a false positive match if we aren't careful, 
        # but usually tight normalizing helps. 
        if len(chunk_norm) < 5: 
            continue
            
        if chunk_norm not in nb_norm:
            # Try a fuzzy check? 
            # Sometimes pandoc conversion produces different chars (e.g. smart quotes).
            # normalize_text handles simple stuff, but let's see.
            missing_chunks.append(chunk.strip())
        else:
            matched_count += 1
            
    total_chunks = matched_count + len(missing_chunks)
    
    print(f"\nRESULTS:")
    print(f"Total Source Chunks Checked: {total_chunks}")
    print(f"Matches Found: {matched_count}")
    print(f"Missing/Mismatched Chunks: {len(missing_chunks)}")
    
    if missing_chunks:
        print("\n\n WARNING: The following sections from the source document appear to be MISSING or ALTERED in the notebook:")
        print("-" * 60)
        for i, chunk in enumerate(missing_chunks, 1):
            print(f"--- MISSING CHUNK #{i} ---")
            # Print just the first few lines to identify it
            lines = chunk.split('\n')
            preview = '\n'.join(lines[:5])
            print(preview)
            print("-" * 20)
        print("-" * 60)
        return False
    else:
        print("\nSUCCESS: All content from the source document was found in the notebook!")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verify notebook contains all text from source markdown.')
    parser.add_argument('source', help='Path to source markdown file')
    parser.add_argument('notebook', help='Path to target .ipynb file')
    
    args = parser.parse_args()
    
    success = verify_fidelity(args.source, args.notebook)
    sys.exit(0 if success else 1)
