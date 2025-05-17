import pytesseract
import pdfplumber
import pandas as pd
from PIL import Image
from io import BytesIO

def processar_arquivo(uploaded_file):
    nome = uploaded_file.name.lower()
    
    if nome.endswith(".pdf"):
        return extrair_texto_pdf(uploaded_file)
    elif nome.endswith(".xlsx"):
        return extrair_texto_excel(uploaded_file)
    elif nome.endswith(".png") or nome.endswith(".jpg"):
        return extrair_texto_imagem(uploaded_file)
    else:
        return "Formato não suportado."

def extrair_texto_pdf(file):
    texto = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() + "\n"
    return texto

def extrair_texto_excel(file):
    df = pd.read_excel(file)
    return df.to_string(index=False)

def extrair_texto_imagem(file):
    image = Image.open(BytesIO(file.read()))
    texto = pytesseract.image_to_string(image, lang="por")
    return texto
