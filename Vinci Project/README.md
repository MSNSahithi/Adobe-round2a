# PDF Heading Extractor (Hackathon Round 1A)

## 📌 Challenge: Connect the Dots Through Docs

Build a system that extracts document outlines from PDFs (Title, H1–H3) in a structured JSON format, suitable for search, recommendation, or semantic tasks.

---

## 💡 Approach

We process the PDF using [PyMuPDF](https://pymupdf.readthedocs.io) (`fitz`) to extract:
- Font sizes
- Font styles
- Page positions
- Text blocks

We infer headings (`H1`, `H2`, `H3`) using **font size clustering and relative position**, rather than relying solely on font size.

### 🔍 Outline Detection Logic
- Largest text on first page → Title
- Next largest consistent fonts → H1, H2, H3
- Hierarchy is based on descending font size
- Handles varying PDF styles by clustering font sizes dynamically

---

## 🧰 Libraries Used

- `PyMuPDF` – Fast PDF parser and font extractor
- `os`, `json` – For file and data handling (Python Standard Library)

No external APIs or models are used. Fully offline.

---

## 🐳 Docker Instructions

### 🧱 Build

```bash
docker build --platform linux/amd64 -t pdf-outliner:v1 .
