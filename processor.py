from pdf_handler import process_pdf
from document_splitter import separar_documentos_por_conteudo
from document_features import extract_features
from analyzer import identificar_tipo_documento, identificar_fornecedor, identificar_cliente
from db_utils import (
    inserir_processo_se_nao_existir,
    get_tipo_doc_id_por_nome,
    inserir_documento
)
import os
from exporter import exportar_documentos_csv, salvar_textos_extraidos


def log_features_resumido(features, idx=None):
    header = f"📄 Documento {idx + 1}" if idx is not None else "📄 Documento"
    print(f"\n{header}")
    print("───────────────")
    print(f"Tipo:        {features['tipo']}")
    print(f"Número:      {features['numero']}")
    print(f"Data:        {features['data']}")
    fornecedor = features['fornecedor']['nome'] if features['fornecedor'] else "Não identificado"
    cliente = features['cliente']['nome'] if features['cliente'] else "Não identificado"
    print(f"Fornecedor:  {fornecedor}")
    print(f"Cliente:     {cliente}")
    print("───────────────")
    print("🔍 Análise concluída.")

def processar_pasta_pdf(diretorio_pdfs):
    arquivos = []

    for root, _, files in os.walk(diretorio_pdfs):
        for file in files:
            if file.lower().endswith(".pdf"):
                arquivos.append(os.path.join(root, file))

    if not arquivos:
        print("⚠️ Nenhum PDF encontrado no diretório ou subdiretórios.")
        return

    documentos_extraidos = []

    for arquivo in arquivos:
        print(f"\n📄 Processando arquivo: {arquivo}")
        paginas = process_pdf(arquivo)
        documentos = separar_documentos_por_conteudo(paginas)

        textos_puros = []

        for i, doc_paginas in enumerate(documentos):
            try:
                texto = "\n".join(doc_paginas)
                textos_puros.append(texto)

                features = extract_features(texto)
                features["documento_origem"] = os.path.basename(arquivo)  # nome do ficheiro PDF
                documentos_extraidos.append(features)
                log_features_resumido(features, idx=i)

                tipo_nome = features["tipo"]
                fornecedor = features["fornecedor"]
                cliente = features["cliente"]
                numero = features["numero"]
                data = features["data"]

                # Obter id do tipo de documento
                id_tipo_doc = get_tipo_doc_id_por_nome(tipo_nome)
                if not id_tipo_doc:
                    print(f"⚠️ Tipo de documento '{tipo_nome}' não encontrado no banco.")
                    continue

                # Inserir processo se aplicável
                if numero and cliente:
                    inserir_processo_se_nao_existir(numero, cliente["id"], descricao=tipo_nome)

                # Inserir documento
                inserir_documento(
                    id_tipo_doc=id_tipo_doc,
                    numero=numero or f"Desconhecido-{i}",
                    data=data,
                    total=0.0,
                    caminho_pdf=arquivo,
                    nif_fornecedor=fornecedor["nif"] if fornecedor else None,
                    id_equipa=None,
                    id_processo=numero if cliente else None
                )
            except Exception as e:
                print(f"❌ Erro ao processar documento {i + 1}: {e}")

        # Salvar textos extraídos deste PDF
        salvar_textos_extraidos(arquivo, textos_puros)

    # Exportar o CSV com todos os documentos da pasta
    exportar_documentos_csv(documentos_extraidos)

        

def processar_pdf_completo(caminho_pdf, caminho_original=None):
    paginas = process_pdf(caminho_pdf)
    documentos = separar_documentos_por_conteudo(paginas)

    for i, doc_paginas in enumerate(documentos):
        try:
            texto = "\n".join(doc_paginas)
            features = extract_features(texto)
            log_features_resumido(features, idx=i)

            tipo_nome = features["tipo"]
            fornecedor = features["fornecedor"]
            cliente = features["cliente"]
            numero = features["numero"]
            data = features["data"]

            # Obter id do tipo de documento
            id_tipo_doc = get_tipo_doc_id_por_nome(tipo_nome)
            if not id_tipo_doc:
                print(f"⚠️ Tipo de documento '{tipo_nome}' não encontrado no banco.")
                continue

            # Inserir processo se aplicável
            if numero and cliente:
                inserir_processo_se_nao_existir(numero, cliente["id"], descricao=tipo_nome)

            # Inserir documento
            inserir_documento(
                id_tipo_doc=id_tipo_doc,
                numero=numero or f"Desconhecido-{i}",
                data=data,
                total=0.0,
                caminho_pdf=caminho_original or caminho_pdf,
                nif_fornecedor=fornecedor["nif"] if fornecedor else None,
                id_equipa=None,
                id_processo=numero if cliente else None
            )
        except Exception as e:
            print(f"❌ Erro ao processar documento {i + 1}: {e}")
