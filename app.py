import streamlit as st
from test_generator import gerar_casos_de_teste
from file_processor import processar_arquivo
from report_generator import exportar_relatorio
from integrations.azure_client import AzureDevOpsClient

st.set_page_config(page_title="Agente Inteligente de Testes", layout="wide")
st.title("🧪 Agente Inteligente para Testes de Software")

uploaded_file = st.file_uploader("📁 Faça upload de um documento de requisitos (PDF, Excel, Imagem)", type=["pdf", "xlsx", "png", "jpg"])

if uploaded_file:
    texto_extraido = processar_arquivo(uploaded_file)
    st.subheader("📄 Texto Extraído")
    st.text_area("Conteúdo", texto_extraido, height=200)

    if st.button("🧠 Gerar Casos de Teste"):
        casos = gerar_casos_de_teste(texto_extraido)
        st.subheader("✅ Casos de Teste Gerados")
        for i, caso in enumerate(casos, 1):
            st.markdown(f"**{i}.** {caso}")

        # Envio para Azure DevOps
        st.subheader("☁️ Enviar para Azure DevOps")
        with st.form("azure_form"):
            org_url = st.text_input("🔗 URL da Organização Azure", "https://dev.azure.com/sua_org")
            pat = st.text_input("🔑 Personal Access Token (PAT)", type="password")
            projeto = st.text_input("📁 Nome do Projeto", "SeuProjeto")
            enviar = st.form_submit_button("📤 Enviar Test Cases")

        if enviar:
            client = AzureDevOpsClient(org_url, pat, projeto)
            for caso in casos:
                titulo = caso.split("\n")[0][:100]  # Título = primeira linha
                passos = caso.replace("\n", "<br>")  # Passos como HTML
                client.criar_test_case(titulo, passos)
            st.success("✅ Casos enviados ao Azure DevOps com sucesso!")

        if st.button("📤 Exportar Relatório"):
            exportar_relatorio(casos)
            st.success("Relatório exportado com sucesso!")
