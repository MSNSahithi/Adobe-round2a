import os
import json
import fitz  # PyMuPDF

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = []

    # Step 1: Collect all font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_sizes.append(span["size"])

    # Step 2: Rank font sizes
    font_sizes = sorted(set(font_sizes), reverse=True)
    heading_map = {}

    if len(font_sizes) > 0:
        heading_map[font_sizes[0]] = "H1"
    if len(font_sizes) > 1:
        heading_map[font_sizes[1]] = "H2"
    if len(font_sizes) > 2:
        heading_map[font_sizes[2]] = "H3"

    title = ""
    outline = []

    # Step 3: Extract headings based on font size
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = span["size"]

                    if not text or len(text) < 3:
                        continue

                    if size == font_sizes[0] and not title:
                        title = text  # First largest text is the title

                    if size in heading_map:
                        outline.append({
                            "level": heading_map[size],
                            "text": text,
                            "page": page_num
                        })

    return {
        "title": title,
        "outline": outline
    }
input_dir = "input"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))

        result = extract_outline(pdf_path)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Processed {filename} → {output_path}")
