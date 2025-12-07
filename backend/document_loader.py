import os
import docx
import pdfplumber

def load_text_from_file(filepath):
    if filepath.endswith(".txt") or filepath.endswith(".md"):
        return open(filepath, "r", encoding="utf-8").read()

    if filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])

    if filepath.endswith(".pdf"):
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    return ""
