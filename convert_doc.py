
import subprocess
import os
import base64
import re
import json
from pathlib import Path

def get_base64_image_tag(image_path, width="100%"):
    """
    Reads an image file and returns an HTML string with embedded base64 data.
    """
    if not os.path.exists(image_path):
        print(f"Warning: Image not found at {image_path}")
        return f"<b>Error: Image not found at {image_path}</b>"

    try:
        with open(image_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode('utf-8')

        ext = Path(image_path).suffix.lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        
        # Determine strict MIME type for common formats to ensure browser compatibility
        if ext == 'svg':
            mime_type = 'image/svg+xml'
        else:
            mime_type = f'image/{ext}'

        html_tag = (
            f'<img src="data:{mime_type};base64,{b64_data}" '
            f'alt="{Path(image_path).name}" '
            f'style="max-width:{width}; height:auto;" />'
        )
        return html_tag
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return f"<b>Error processing image {image_path}</b>"

def convert_to_notebook(docx_path, output_notebook_path):
    print(f"Converting {docx_path}...")
    
    # 1. Run Pandoc to convert docx to markdown and extract media
    # We use a temporary markdown file
    temp_md = "temp_output.md"
    media_dir = "media_chapter_10"
    
    # Create media directory if it handles it differently or just let pandoc do it
    if os.path.exists(media_dir):
         # Optional: clean up old media? For now, let's just leave it or overwrite.
         pass
         
    cmd = [
        "pandoc",
        docx_path,
        "-f", "docx",
        "-t", "gfm",
        "--wrap=none",
        f"--extract-media={media_dir}",
        "-o", temp_md
    ]
    
    print("Running Pandoc:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    
    # 2. Read the generated markdown
    with open(temp_md, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 3. Process the markdown to embed images
    # Pandoc markdown images look like: ![](path/to/image.png) or ![alt](path/to/image.png)
    # Regex to find images: !\[(.*?)\]\((.*?)\)
    
    # Replace markdown images: ![alt](path)
    def md_image_replacer(match):
        img_path = match.group(2)
        print(f"Found markdown image: {img_path}")
        return get_base64_image_tag(img_path)
    
    processed_content = re.sub(r'!\[(.*?)\]\((.*?)\)', md_image_replacer, md_content)

    # Replace HTML images: <img src="path" ... />
    def html_image_replacer(match):
        img_path = match.group(1)
        print(f"Found HTML image: {img_path}")
        return get_base64_image_tag(img_path)
    
    processed_content = re.sub(r'<img src="(.*?)"(?:.*?)/>', html_image_replacer, processed_content)

    # 3b. Clean up Pandoc artifacts
    # Remove dimension attributes like {width="..." height="..."} that might appear after markdown images
    processed_content = re.sub(r'\{width=.*?\}', '', processed_content)
    
    # Remove spans like [Text]{.underline} -> <u>Text</u>
    # Or generically [Text]{...} -> Text (or handle specific classes)
    def span_replacer(match):
        text = match.group(1)
        attrs = match.group(2)
        if 'underline' in attrs:
            return f'<u>{text}</u>'
        return text

    processed_content = re.sub(r'\[(.*?)\]\{(.*?)\}', span_replacer, processed_content)

    # 4. Create Notebook Structure
    cells = []
    
    current_cell_source = []
    
    for line in processed_content.splitlines():
        # Heuristic for new cell:
        # 1. Line starts with # (Header)
        # 2. Line looks like a bold header: **Something** (and short)
        
        is_header = line.strip().startswith('#')
        is_bold_header = line.strip().startswith('**') and len(line) < 100
        
        if (is_header or is_bold_header) and current_cell_source:
             # If the previous cell was very short (e.g. valid empty lines), maybe don't split?
             # But generally, split.
             
             # Clean up trailing empty lines from previous cell
             while current_cell_source and not current_cell_source[-1].strip():
                 current_cell_source.pop()
                 
             if current_cell_source:
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "\n".join(current_cell_source)
                })
                current_cell_source = []
        
        current_cell_source.append(line)
        
    # Append the last cell
    if current_cell_source:
        cells.append({
             "cell_type": "markdown",
             "metadata": {},
             "source": "\n".join(current_cell_source)
         })

    notebook_json = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(output_notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook_json, f, indent=2)

    print(f"Created notebook: {output_notebook_path}")
    
    # Cleanup
    if os.path.exists(temp_md):
        os.remove(temp_md)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert docx to ipynb with embedded images.")
    parser.add_argument("docx_file", nargs='?', help="Path to input docx file")
    parser.add_argument("output_nb", nargs='?', help="Path to output ipynb file")
    
    args = parser.parse_args()

    if args.docx_file and args.output_nb:
        # Command line arguments provided
        full_docx_path = os.path.abspath(args.docx_file)
        convert_to_notebook(full_docx_path, args.output_nb)
    else:
        # Default behavior (useful for quick testing or if run without args)
        print("No arguments provided. Usage: python convert_doc.py <input.docx> <output.ipynb>")
        # Example default, can be removed or kept as fallback
        # docx_file = "../curriculumNotesFromBob/Chapter 11 - Understanding Randomness (Guided Notes).docx"
        # output_nb = "Chapter_11.ipynb"
        # cwd = os.getcwd()
        # full_docx_path = os.path.join(cwd, docx_file)
        # convert_to_notebook(full_docx_path, output_nb)
