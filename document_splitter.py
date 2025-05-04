from analyzer import classify_document, identify_supplier

def split_document_by_content(pages_text):
    """
    Divide uma lista de textos de páginas em documentos separados,
    com base em tipo de documento, fornecedor e heurísticas simples.
    """
    documentos = []
    documento_atual = []

    tipo_anterior = None
    fornecedor_anterior = None

    for idx, texto in enumerate(pages_text):
        tipo_atual = classify_document(texto)
        fornecedor_atual = identify_supplier(texto)

        nova_pagina = texto.strip().lower().startswith(("fatura", "nota", "recibo", "orçamento"))

        precisa_novo_documento = (
            tipo_anterior and tipo_atual != tipo_anterior or
            fornecedor_anterior and fornecedor_atual != fornecedor_anterior or
            nova_pagina
        )

        if precisa_novo_documento and documento_atual:
            documentos.append(documento_atual)
            documento_atual = []

        documento_atual.append(texto)
        tipo_anterior = tipo_atual
        fornecedor_anterior = fornecedor_atual

    if documento_atual:
        documentos.append(documento_atual)

    return documentos
