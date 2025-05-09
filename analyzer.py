import re
from db_utils import get_fornecedores, get_processos, get_equipas
from document_types import (
    TIPOS_DOCUMENTO_FORNECEDOR,
    TIPOS_DOCUMENTO_PROCESSO,
    TIPOS_DOCUMENTOS_EQUIPA
)

def identificar_tipo_documento(texto):
    texto = texto.lower()

    if identificar_fornecedor(texto):
        return classificar_por_padroes(texto, TIPOS_DOCUMENTO_FORNECEDOR, "Cotação")
    elif identificar_processo(texto):
        return classificar_por_padroes(texto, TIPOS_DOCUMENTO_PROCESSO)
    elif identificar_equipa(texto):
        return classificar_por_padroes(texto, TIPOS_DOCUMENTOS_EQUIPA)

def classificar_por_padroes(texto, padroes, padrao_padrao):
    for tipo, palavras in padroes.items():
        for palavra in palavras:
            if palavra in texto:
                return tipo
    return padrao_padrao

import re

def identificar_fornecedor(texto):
    fornecedores = get_fornecedores()
    
    texto_limpo = re.sub(r'\s+', '', texto.lower())

    for f in fornecedores:
        nif = f["nif"]
        nome = f["nome"].lower().replace(" ", "").replace(",", "").replace(".", "")
        
        # Primeiro verifica se o NIF está presente
        if nif in texto_limpo:
            return f
    
    # Se não encontrou pelo NIF, tenta agora pelo nome
    for f in fornecedores:
        nome = f["nome"].lower().replace(" ", "").replace(",", "").replace(".", "")
        if nome in texto_limpo:
            return f

    return None


def identificar_processo(texto):
    processos = get_processos()
    
    texto_limpo = re.sub(r'\s+', '', texto.lower())

    for p in processos:
        ref = p["ref"]

        if ref in texto_limpo:
            return p

    return None

def identificar_equipa(texto):
    equipas = get_equipas()
    
    texto_limpo = re.sub(r'\s+', '', texto.lower())

    for e in equipas:
        nome = e["nome"].lower().replace(" ", "").replace(",", "").replace(".", "")
        
        if nome in texto_limpo:
            return e

    return None