from document_number_patterns import PADROES_NUMERO_DOCUMENTO
import re

def extract_features(texto):
    numero = extract_document_number(texto)
    total = extract_total(texto)

    return {
        "numero": numero,
        "total": total
    }

def extract_document_number(texto):
    texto = texto.lower()
    for sigla in PADROES_NUMERO_DOCUMENTO.get("Fatura", []):
        pattern = rf'{sigla}[\s:]*([a-z0-9\-\/\.]+)'
        match = re.search(pattern, texto)
        if match:
            return match.group(1).strip()
    return None

def extract_total(texto):
    match = re.search(r'total[:\s]*([\d\.,]+)', texto.lower())
    if match:
        return float(match.group(1).replace(',', '.'))
    return 0.0
