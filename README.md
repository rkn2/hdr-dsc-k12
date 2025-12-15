# Word to Jupyter Notebook Conversion Workflow

This guide documents the process for replacing the manual conversion of Word documents with an automated script that produces high-quality Jupyter Notebooks (`.ipynb`) compatible with Google Colab.

## Overview

The goal is to convert Microsoft Word (`.docx`) files, which contain text, images, and tables, into Jupyter Notebooks. The output notebooks should:
1.  **Embed Images:** Use Base64 encoding so images are self-contained within the notebook (no external image folders needed).
2.  **Preserve Formatting:** Maintain bolding, italics, and headers.
3.  **Handle Tables:** Render tables clearly using GitHub Flavored Markdown (GFM).
4.  **Be Automated:** Allow for batch processing of multiple chapters.

## Prerequisites

1.  **Python 3**: Ensure Python is installed.
2.  **Pandoc**: This tool is essential for the underlying conversion.
    *   *Mac (Homebrew):* `brew install pandoc`
    *   *Windows/Linux:* See [pandoc.org](https://pandoc.org/installing.html)
3.  **Dependencies**: The python script uses standard libraries (`os`, `sys`, `json`, `base64`, `re`, `pathlib`, `argparse`, `subprocess`), so no `pip install` is usually required.

## The Script: `convert_doc.py`

The core of this workflow is the `convert_doc.py` script located in the root of the repository.

### How it Works
1.  **Pandoc Conversion**: It runs `pandoc` to convert the `.docx` file into a temporary GitHub Flavored Markdown (`gfm`) file. It extracts images into a temporary folder.
    *   *Command used internally:* `pandoc input.docx -f docx -t gfm --extract-media=temp_folder -o temp.md`
    *   *Why GFM?* It preserves table borders better than standard markdown.
2.  **Image Embedding**: It scans the generated markdown for both Markdown-style images (`![alt](path)`) and HTML-style images (`<img src="path" ... />`). It reads the image files, converts them to Base64 strings, and replaces the links with embedded HTML tags.
3.  **Cleanup**: It removes Pandoc-specific artifacts (like `{width=...}` tags) and fixes common formatting issues (like `[text]{.underline}` -> `<u>text</u>`).
4.  **Notebook Creation**: It parses the markdown, splitting content into separate cells based on headers to improve readability, and generates a valid `.ipynb` JSON file.

### Usage

You can run the script from the command line, passing the input Word document and the desired output Notebook filename.

**Basic Syntax:**
```bash
python3 convert_doc.py "Path/To/Input.docx" "Output_Name.ipynb"
```

**Examples:**

*   Convert a single chapter:
    ```bash
    python3 convert_doc.py "../curriculumNotesFromBob/Chapter 9.docx" "Chapter_9.ipynb"
    ```

*   Convert multiple chapters (using a simple shell script or individual commands):
    ```bash
    python3 convert_doc.py "Chapter 10.docx" "Chapter_10.ipynb"
    python3 convert_doc.py "Chapter 11.docx" "Chapter_11.ipynb"
    ```

## Files in this Repository

*   `convert_doc.py`: The main automation script.
*   `README.md`: This file.
*   `Chapter_*.ipynb`: The converted notebooks.

## Troubleshooting

*   **Tables look wrong:** Ensure you are using the latest version of the script which uses the `gfm` (GitHub Flavored Markdown) format in the Pandoc step.
*   **Images missing:** The script handles both Markdown `![]()` and HTML `<img src="">` tags. If images are missing, check if the source Word doc uses unusual image wrapping.
*   **Math Equations:** Standard Word equations are converted to LaTeX (`$E=mc^2$`). However, equations pasted as **pictures** in Word cannot be converted to text/LaTeX automatically and will remain as images.
