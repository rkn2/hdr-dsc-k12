
## **Embedding Images in Jupyter Notebooks for Google Colab**

When sharing Jupyter Notebooks (especially on Google Colab), dealing with external image files can be frustrating. If you send someone a notebook file (`.ipynb`), the images often appear as broken links because the recipient does not have your local `images/` folder.

To solve this, we can **embed the images directly into the notebook** as text.

### **The Solution: Base64 Encoding**

**Base64** is a method used to convert binary data (like an image file) into a long string of ASCII text characters. This allows us to "store" the image inside the text-based Jupyter Notebook file itself.

**The Workflow:**
1.  **Read** the image file from your computer as raw binary data (0s and 1s).
2.  **Encode** that binary data into a Base64 text string.
3.  **Embed** that string into an HTML `<img>` tag within a Markdown cell.

### **Key Benefits**
*   **Portability:** The notebook becomes a single, standalone file. You can email it or upload it to Colab, and the images will "travel" with it.
*   **Zero Dependencies:** No need for the user to mount Google Drive or clone a GitHub repository just to see a diagram.
*   **Persistent:** The images won't break if the original source file is moved or deleted.

### **Python Helper Function**

You can use the following Python function to automate this process. It reads an image file and generates the exact HTML code needed for your notebook.

```python
import base64
import os
from pathlib import Path

def get_base64_image_tag(image_path, width="100%"):
    """
    Reads an image file and returns an HTML string with embedded base64 data.
    
    Args:
        image_path (str): The path to the local image file.
        width (str): CSS width property (default '100%').
        
    Returns:
        str: An HTML <img> tag containing the base64-encoded image.
    """
    # Check if file exists
    if not os.path.exists(image_path):
        return f"<b>Error: Image not found at {image_path}</b>"

    # 1. Read the binary file
    with open(image_path, "rb") as img_file:
        # Encode bytes to base64 string
        # .decode('utf-8') turns the byte object into a standard string
        b64_data = base64.b64encode(img_file.read()).decode('utf-8')

    # 2. Determine file extension for MIME type (png, jpg, etc.)
    ext = Path(image_path).suffix.lower().replace('.', '')
    # Handle common alias
    if ext == 'jpg': ext = 'jpeg'
    
    # 3. Create the HTML tag
    # The 'src' attribute uses the data URI scheme: data:[<mediatype>][;base64],<data>
    html_tag = (
        f'<img src="data:image/{ext};base64,{b64_data}" '
        f'alt="{Path(image_path).name}" '
        f'style="max-width:{width}; height:auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 10px 0;" />'
    )
    
    return html_tag

# --- Usage Example ---
# If you run this in a cell, it will print the text you need to copy-paste.
# Or, if you are generating notebooks via script, insert this string into the 'source' list.

# my_tag = get_base64_image_tag("my_chart.png")
# print(my_tag) 
```

### **Understanding the Output**

The function generates an HTML tag that looks like this:

```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." style="max-width:100%; ..." />
```

*   `data:image/png`: Tells the browser this is an image file of type PNG.
*   `;base64`: Tells the browser the data is encoded using Base64.
*   `iVBORw0K...`: The actual image data. This string can be extremely long!

**Note:** While this increases the file size of your `.ipynb` file, it guarantees that your content will render correctly on any platform.
