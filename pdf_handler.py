import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import config
import os
import PyPDF2
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

def process_pdf(pdf_path):
    """
    Processa o PDF e retorna lista de textos por página.
    Usa OCR apenas quando necessário.
    """
    texts = []

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        print(f"[INFO] Total de páginas: {len(reader.pages)}")
        for idx, page in enumerate(reader.pages):
            print(f"[PROCESSANDO] Página {idx+1}...")

            text = page.extract_text()

            if text and len(text.strip()) > 20:
                print(" → Texto extraído diretamente.")
                texts.append(text)
            else:
                print(" → Nenhum texto detectado. Aplicando OCR...")
                image = convert_from_path(
                    pdf_path, 
                    first_page=idx+1, 
                    last_page=idx+1, 
                    poppler_path=config.POPPLER_PATH
                )[0]
                ocr_text = pytesseract.image_to_string(image, lang="por")
                texts.append(ocr_text)

    return texts
