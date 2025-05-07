import re
from db_utils import get_fornecedores, get_clientes
from document_types import (
    TIPOS_DOCUMENTO_FORNECEDOR,
    TIPOS_DOCUMENTO_CLIENTE,
    TIPOS_ESPECIAIS
)

def identificar_tipo_documento(texto):
    texto = texto.lower()

    if identificar_fornecedor(texto):
        return classificar_por_padroes(texto, TIPOS_DOCUMENTO_FORNECEDOR, "Cotação")
    elif identificar_cliente(texto):
        return classificar_por_padroes(texto, TIPOS_DOCUMENTO_CLIENTE, "Orçamento")
    else:
        return classificar_por_padroes(texto, TIPOS_ESPECIAIS, "Desconhecido")

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


def identificar_cliente(texto):
    clientes = get_clientes()
    
    texto_limpo = re.sub(r'\s+', '', texto.lower())

    for c in clientes:
        nif = c["nif"]
        nome = c["nome"].lower().replace(" ", "").replace(",", "").replace(".", "")
        
        # Primeiro verifica se o NIF está presente
        if nif in texto_limpo:
            return c

    # Se não encontrou pelo NIF, tenta agora pelo nome
    for c in clientes:
        nome = c["nome"].lower().replace(" ", "").replace(",", "").replace(".", "")
        if nome in texto_limpo:
            return c

    return None
