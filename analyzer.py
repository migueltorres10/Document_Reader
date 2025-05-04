from db_utils import get_tipos_documento, get_fornecedores

def classify_document(texto):
    """
    Identifica o tipo de documento com base nos termos cadastrados no banco.
    """
    texto = texto.lower()
    tipos = get_tipos_documento()

    for tipo in tipos:
        if tipo in texto:
            return tipo.title()
    return "Desconhecido"

def identify_supplier(texto):
    """
    Identifica o fornecedor com base em NIF ou nome cadastrado no banco.
    """
    texto_lower = texto.lower()
    fornecedores = get_fornecedores()

    for fornecedor in fornecedores:
        # Por NIF
        if fornecedor["nif"] in texto:
            return fornecedor["nome"]

        # Por nome (simplificado)
        if fornecedor["nome"].lower() in texto_lower:
            return fornecedor["nome"]

    return "Fornecedor Desconhecido"
