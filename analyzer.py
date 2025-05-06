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

def identificar_fornecedor(texto):
    fornecedores = get_fornecedores()
    for f in fornecedores:
        if f["nif"] in texto or f["nome"].lower() in texto.lower():
            return f
    return None

def identificar_cliente(texto):
    clientes = get_clientes()
    for c in clientes:
        if c["nif"] in texto or c["nome"].lower() in texto.lower():
            return c
    return None
