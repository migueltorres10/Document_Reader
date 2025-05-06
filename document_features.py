from analyzer import identificar_tipo_documento, identificar_fornecedor, identificar_cliente
from document_number_patterns import PADROES_NUMERO_DOCUMENTO
from datetime import date
from dateutil import parser
import re

def extract_document_number(texto, tipo):
    """
    Extrai número com base em siglas conhecidas para o tipo identificado.
    """
    texto = texto.lower()
    padroes = PADROES_NUMERO_DOCUMENTO.get(tipo, [])

    for sigla in padroes:
        # Exemplo: ft 1234/2024 ou nota de crédito: 8765
        pattern = rf'{sigla}[\s:]*([a-z0-9\-\/\.]+)'
        match = re.search(pattern, texto)
        if match:
            return match.group(1).strip()

    return None

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
    cliente = identificar_cliente(texto)
    numero = extract_document_number(texto, tipo)
    data = extract_date(texto)

    return {
        "tipo": tipo,
        "fornecedor": fornecedor,
        "cliente": cliente,
        "numero": numero,
        "data": data
    }
