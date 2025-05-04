import os
from pdf_handler import process_pdf

def main():
    pasta = "pdfs"
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".pdf")]

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        print(f"\n===== PROCESSANDO: {arquivo} =====")
        textos = process_pdf(caminho)

        for i, texto in enumerate(textos):
            print(f"\n--- Página {i+1} ---")
            print(texto[:500])  # mostra os primeiros 500 caracteres

if __name__ == "__main__":
    main()
