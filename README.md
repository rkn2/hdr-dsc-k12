# HDR DSC K-12: Statistics Curriculum Notebooks

This repository contains interactive Jupyter Notebooks designed for the HDR DSC K-12 Statistics curriculum. These notebooks replace static worksheets with dynamic, data-driven learning experiences.

## 📌 Navigation
*   [**For High School Teachers & Students**](#for-high-school-teachers--students) - Access the curriculum and learn how to use it.
*   [**For Developers & Contributors**](#for-developers--contributors) - Learn how the conversion scripts work and how to update them.

---

# For High School Teachers & Students

## What is this?
This is a collection of "Guided Notes" converted into interactive **Jupyter Notebooks**. Unlike standard Word documents, these notebooks allow you to run real experiments and simulations directly in your browser.

## How to Use
1.  **Select a Chapter** from the table below.
2.  **Click the "Open in Colab" badge**. This launches the notebook in Google's cloud environment.
3.  **Run the Simulations**: Look for the interactive widgets (like the Coin Flip or Survey simulator).
    *   Click the **Play Symbol (▶)** next to the title (e.g., `# @title 🟢 Click 'Play' to Start`).
    *   Adjust sliders and settings to explore the data!

## 📚 Curriculum Materials

| Chapter | Title | Colab Link | Key Interpretive Simulations |
| :--- | :--- | :--- | :--- |
| **9** | Samples | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_9.ipynb) | Bias Simulator, Sample Size Explorer |
| **10** | Observational Studies | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_10_updated.ipynb) | **Confounding Variable Explorer** (Simpson's Paradox), Lurking Variables |
| **11** | Understanding Randomness | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_11.ipynb) | **World Series Sim**, **Cereal Box Collection**, Dorm Lottery, Free Throw Streaks |
| **12** | Counting Principles | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_12.ipynb) | Permutations vs. Combinations, Birthday Problem |
| **13** | Probability | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_13.ipynb) | Traffic Light Model, Dice Sum Simulator |
| **14** | Probability Rules | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_14.ipynb) | Venn Diagram Explorer, Conditional Probability Tree |
| **15** | Probability Models | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_15.ipynb) | Binomial/Normal Approximation, Geometric Distribution |
| **16** | Confidence Intervals | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rkn2/hdr-dsc-k12/blob/main/Chapter_16.ipynb) | Capture the Parameter, Margin of Error Explorer |

---

# For Developers & Contributors

This section documents the technical workflow for converting Word documents into the Jupyter Notebooks listed above.

## Overview
The goal is to automate the conversion of Microsoft Word (`.docx`) files into high-quality Jupyter Notebooks (`.ipynb`) that:
1.  **Embed Images**: Use Base64 encoding so images are self-contained.
2.  **Preserve Formatting**: Maintain bolding, italics, headers, and tables.
3.  **Hide Code**: Automatically configure cells so Python code is hidden from students by default.

## The Script: `convert_doc.py`
The core tool is `convert_doc.py`, located in the root of this repository.

### Prerequisites
1.  **Python 3**
2.  **Pandoc**: Essential for the underlying conversion.
    *   *Mac (Homebrew):* `brew install pandoc`
    *   *Windows/Linux:* See [pandoc.org](https://pandoc.org/installing.html)
3.  **Dependencies**: Standard libraries (`os`, `sys`, `json`, `base64`, `re`, `pathlib`).

### How it Works
1.  **Pandoc Conversion**: Converts `.docx` to temporary GitHub Flavored Markdown (`gfm`), extracting images to a folder.
2.  **Image Embedding**: Scans for images, converts them to Base64 strings, and embeds them directly into the markdown as HTML tags.
3.  **Cleanup**: Removes Pandoc-specific artifacts and fixes formatting quirks.
4.  **Notebook Generation**: Parses the markdown into JSON cells, creating a valid `.ipynb` file.

### Usage
Run the script from the command line:

```bash
python3 convert_doc.py "Path/To/Input.docx" "Output_Name.ipynb"
```

**Example:**
```bash
python3 convert_doc.py "../curriculumNotes/Chapter 11.docx" "Chapter_11.ipynb"
```

## Adding Interactive Widgets
After conversion, interactivity is added via Python scripts (e.g., `add_widgets_ch10.py`). These scripts:
1.  Load the notebook JSON.
2.  Locate specific "anchor text" (e.g., "Example 1").
3.  Inject a new Code Cell containing the widget logic (`ipywidgets`).
4.  Inject a `# @title` header to ensure the code collapses in Colab.

## Troubleshooting
*   **Tables look wrong:** Ensure Pandoc is up to date. The script uses GFM format for tables.
*   **Images missing:** The script handles standard Word images. Smart Art or Equation Objects usually need to be screenshotted/converted to pictures first.
