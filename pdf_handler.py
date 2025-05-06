import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import config
import os
import PyPDF2
from io import BytesIO

# Define caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

def process_pdf(pdf_path):
    """
    Processa o PDF e retorna uma lista de textos por página.
    Usa OCR apenas quando o texto extraível está ausente ou vazio.
    """
    texts = []

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        print(f"[INFO] Total de páginas: {len(reader.pages)}")
        for idx, page in enumerate(reader.pages):
            print(f"[PROCESSANDO] Página {idx + 1}...")

            try:
                text = page.extract_text()
                if text and len(text.strip()) > 20:
                    print(" → Texto extraído diretamente.")
                    texts.append(text)
                else:
                    print(" → Nenhum texto detectado. Aplicando OCR...")
                    image = convert_from_path(
                        pdf_path,
                        first_page=idx + 1,
                        last_page=idx + 1,
                        poppler_path=config.POPPLER_PATH
                    )[0]
                    ocr_text = pytesseract.image_to_string(image, lang="por")
                    texts.append(ocr_text)
            except Exception as e:
                print(f"❌ Erro ao processar página {idx + 1}: {e}")
                texts.append("")

    return texts
