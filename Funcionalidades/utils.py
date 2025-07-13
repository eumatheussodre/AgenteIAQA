# Funcionalidades/utils.py

import io
import json
import streamlit as st
import pandas as pd
import pdfplumber
import docx


def processar_arquivo(uploaded_file):
    # ... (mantenha a sua função processar_arquivo aqui) ...
    if uploaded_file is None:
        return ""
    file_name = uploaded_file.name
    file_extension = file_name.split('.')[-1].lower()
    try:
        if file_extension in ["txt", "md"]:
            return uploaded_file.getvalue().decode("utf-8")
        elif file_extension == "pdf":
            texto_pdf = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    texto_pdf += page.extract_text() + "\n"
            return texto_pdf
        elif file_extension == "docx":
            texto_docx = ""
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                texto_docx += para.text + "\n"
            return texto_docx
        else:
            return f"Formato de ficheiro '{file_extension}' não suportado."
    except Exception as e:
        print(f"Erro ao processar o ficheiro {file_name}: {e}")
        return f"Não foi possível ler o ficheiro. Erro: {e}"


# --- NOVAS FUNÇÕES MOVIDAS PARA CÁ ---

def exibir_e_baixar_json(titulo: str, dados_json: dict or list, nome_arquivo: str):
    """Exibe um título, os dados formatados em JSON e um botão de download."""
    st.subheader(titulo)
    st.json(dados_json)
    json_string = json.dumps(
        dados_json, ensure_ascii=False, indent=4).encode('utf-8')
    st.download_button(
        label="⬇️ Baixar JSON",
        data=json_string,
        file_name=nome_arquivo,
        mime="application/json"
    )


def exibir_e_baixar_csv(titulo: str, dataframe: pd.DataFrame, nome_arquivo: str):
    """Exibe um título, uma tabela de dados e um botão de download para CSV."""
    st.subheader(titulo)
    st.dataframe(dataframe.head())
    csv_string = dataframe.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv_string,
        file_name=nome_arquivo,
        mime="text/csv"
    )
