import csv
import os

def exportar_documentos_csv(lista_features, nome_arquivo="relatorio_documentos.csv"):
    """
    Exporta uma lista de features de documentos para um CSV.
    """
    campos = ["Documento", "Tipo", "Número", "Data", "Fornecedor", "Cliente"]

    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for idx, ftr in enumerate(lista_features):
            writer.writerow({
                "Documento": f"Documento {idx + 1}",
                "Tipo": ftr["tipo"],
                "Número": ftr["numero"] or "",
                "Data": ftr["data"] or "",
                "Fornecedor": ftr["fornecedor"]["nome"] if ftr["fornecedor"] else "",
                "Cliente": ftr["cliente"]["nome"] if ftr["cliente"] else ""
            })

    print(f"📁 Relatório CSV gerado: {os.path.abspath(nome_arquivo)}")

def salvar_textos_extraidos(pdf_name, documentos_texto, pasta_destino="textos_extraidos"):
    """
    Salva os textos extraídos de cada documento em arquivos .txt individuais.
    """
    os.makedirs(pasta_destino, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_name))[0]

    for idx, texto in enumerate(documentos_texto):
        nome_arquivo = f"{base_name}_documento_{idx + 1}.txt"
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(texto)

    print(f"📝 Textos salvos em: {os.path.abspath(pasta_destino)}")
