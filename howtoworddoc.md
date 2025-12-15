
## **Converting Word Documents to Markdown with Pandoc**

**Pandoc** is a universal document converter that works exceptionally well for transforming Microsoft Word documents (`.docx`) into clean, usable Markdown (`.md`). This process preserves formatting, extracts images, and makes content ready for Jupyter Notebooks or web publishing.

### **The Command**

The core command to convert a Word document to Markdown relies on extracting media (images) to a specific folder.

```bash
pandoc "InputFile.docx" -f docx -t markdown -s --wrap=none --extract-media="." -o "OutputFile.md"
```

### **Breakdown of Arguments**

*   `"InputFile.docx"`: The path to your source Word document.
*   `-f docx`: Specifies the **from** (input) format.
*   `-t markdown`: Specifies the **to** (output) format.
*   `-s`: Stands for **standalone**. It ensures the output is a complete document with headers/metadata, not just a document fragment.
*   `--wrap=none`: Prevents Pandoc from hard-wrapping text lines. This is crucial for keeping paragraphs intact, which makes the Markdown much easier to edit and version control.
*   `--extract-media="."`: This is the most important flag for documents with images.
    *   It tells Pandoc to find all images inside the Word doc and save them as actual files in a `media/` folder in the current directory (`.`).
    *   Without this, images are lost or ignored.
*   `-o "OutputFile.md"`: Specifies the **output** filename.

### **Workflow for Content Migration**

1.  **Preparation:** Place your `.docx` file in a working directory.
2.  **Conversion:** Run the Pandoc command in your terminal.
3.  **Result:** You will get:
    *   A `.md` file containing the text and links to images.
    *   A `media/` folder containing all the extracted image files (e.g., `image1.png`, `image2.jpeg`).
4.  **Integration:**
    *   You can now copy the text from the `.md` file into a Jupyter Notebook cell.
    *   **For Images:** Since the images are now local files in the `media/` folder, you can use the **Base64 embedding technique** (see `howtoimages.md`) to embed them directly into your notebook for portability.

### **Why use this method?**
*   **Accuracy:** Pandoc handles lists, bold/italic text, and heading levels (H1, H2, H3) very accurately from Word styles.
*   **Media Recovery:** It's often the fastest way to get high-quality original images out of a Word doc without taking screenshots.
*   **Automation:** This command can be scripted to batch process an entire curriculum of Word documents at once.
