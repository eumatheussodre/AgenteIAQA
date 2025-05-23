def processar_arquivo(arquivo):
    if arquivo.type.startswith("text"):
        return arquivo.read().decode("utf-8")
    elif arquivo.type.endswith("pdf"):
        import PyPDF2
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    elif arquivo.type.endswith(("jpg", "jpeg", "png")):
        return "[Imagem enviada]"
    elif arquivo.type.endswith("xlsx"):
        import pandas as pd
        df = pd.read_excel(arquivo)
        return df.to_string()
    else:
        return "Tipo de arquivo não suportado."
