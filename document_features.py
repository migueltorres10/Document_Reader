from analyzer import identificar_tipo_documento, identificar_fornecedor, identificar_processo, identificar_equipa
import importlib
from datetime import date
from dateutil import parser
import re

def extract_date(texto):
    hoje = date.today()
    datas_validas = []

    encontrados = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b', texto)
    for d in encontrados:
        try:
            dt = parser.parse(d, dayfirst=True).date()
            if dt <= hoje:
                datas_validas.append(dt)
        except:
            continue

    if datas_validas:
        return max(datas_validas)
    return None

def extract_features(texto):
    tipo = identificar_tipo_documento(texto)
    fornecedor = identificar_fornecedor(texto)
    processo = identificar_processo(texto)
    equipa = identificar_equipa(texto)
    data = extract_date(texto)

    try:
        modulo = importlib.import_module(f"document_features.extractor_{tipo.lower().replace(' ', '_')}")
        features_tipo = modulo.extract_features(texto)
    except ModuleNotFoundError:
        print(f"⚠️ Nenhum extractor encontrado para tipo: {tipo}")
        features_tipo = {}

    return {
        "tipo": tipo,
        "fornecedor": fornecedor,
        "processo": processo,
        "equipa": equipa,
        "data": data,
        **features_tipo
    }
