import pdfplumber
import pytesseract
import pdf2image
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\tmp\poppler\Library\bin"

def is_scanned(pdf_path: str) -> bool:
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                return False
    return True

def parse_text_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_scanned_pdf(pdf_path: str) -> str:
    pages = pdf2image.convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    text = ""
    for i, page in enumerate(pages):
        print(f"  OCR stránka {i+1}/{len(pages)}...")
        text += pytesseract.image_to_string(page, lang="ces") + "\n"
    return text

def parse_pdf(pdf_path: str) -> str:
    if is_scanned(pdf_path):
        print("Detekováno skenované PDF, spouštím OCR...")
        return parse_scanned_pdf(pdf_path)
    else:
        print("Textové PDF, čtu přímo...")
        return parse_text_pdf(pdf_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Použití: python pdf_parser.py soubor.pdf")
    else:
        result = parse_pdf(sys.argv[1])
        print(result[:2000])