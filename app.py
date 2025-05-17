import streamlit as st
from Funcionalidades.Testes.file_processor import *
from Funcionalidades.Testes.report_generator import *
from Funcionalidades.Testes.data_generator import *
from Funcionalidades.Testes.bank_generator import *
from Funcionalidades.Testes.g_Test_Stress import *
from Funcionalidades.Testes.test_generator import *
from Funcionalidades.Testes.test_API import *   


st.set_page_config(page_title="Agente IA - [QA] - Prototipo - i4Pro", layout="wide")
st.title("🧪 Agente IA - Prototipo [QA] - i4Pro")

# 🏠 Menu lateral atualizado com nova opção
menu = st.sidebar.radio("📌 Selecione uma função:", 
[
    "Gerar Casos de Teste",
    "Gerador de Dados",
    "Gerador de Massa Bancária",
    "Gerador de Testes de Carga",
    "Teste de API",
    "Exportar Relatório"
])

# 📌 Geração de Casos de Teste
if menu == "Gerar Casos de Teste":
    st.subheader("📁 Upload de Documentoss")
    uploaded_dev = st.file_uploader("Upload do Documento do Desenvolvedor", type=["pdf", "xlsx", "png", "jpg"])
    uploaded_spec = st.file_uploader("Upload da Especificação Funcional", type=["pdf", "xlsx", "png", "jpg"])

    if uploaded_dev and uploaded_spec:
        st.success("✅ Ambos os documentos foram enviados!")
        texto_dev = processar_arquivo(uploaded_dev)
        texto_spec = processar_arquivo(uploaded_spec)

        if st.button("🧠 Gerar Casos de Teste"):
            casos = gerar_casos_de_teste(texto_dev, texto_spec) or []

            if casos:
                st.subheader("✅ Casos de Teste Gerados")
                for i, caso in enumerate(casos, 1):
                    st.markdown(f"**{i}.** {caso}")
            else:
                st.error("⚠️ Nenhum caso de teste foi gerado!")

# 📊 Gerador de Massa de Dados para QA
elif menu == "Gerador de Dados":
    st.subheader("⚙️ Gerador de Massa de Dados para QA")

    quantidade = st.slider("Quantidade de registros", min_value=1, max_value=50, value=10)

    if st.button("📊 Gerar Dados"):
        massa_dados = gerar_massa_de_dados(quantidade)

        st.subheader(f"📄 {quantidade} Registros Gerados")
        for dado in massa_dados:
            st.write(dado)

# 💳 Novo: Gerador de Massa Bancária
elif menu == "Gerador de Massa Bancária":
    st.subheader("🏦 Gerador de Massa de Dados Bancários")

    quantidade = st.slider("Quantidade de contas bancárias", min_value=1, max_value=50, value=10)

    if st.button("💳 Gerar Dados Bancários"):
        massa_bancaria = gerar_massa_bancaria(quantidade)

        st.subheader(f"📄 {quantidade} Contas Bancárias Geradas")
        for dado in massa_bancaria:
            st.write(dado)

# 🏋️‍♂️ Novo: Gerador de Massa para Testes de Carga
elif menu == "Gerador de Testes de Carga":
    st.subheader("⚡ Gerador de Testes de Carga")

    quantidade = st.slider("Quantidade de registros", min_value=1000, max_value=100000, value=10000)

    if st.button("🔥 Gerar Dados para Testes de Carga"):
        with st.spinner("⏳ Gerando massa de dados..."):
            dados = gerar_massa_carga(quantidade)
            salvar_arquivo(f"massa_carga.csv", dados, "csv")
            salvar_arquivo(f"massa_carga.json", dados, "json")

        st.success(f"✅ {quantidade} registros gerados! Arquivos `massa_carga.csv` e `massa_carga.json` criados!")

        # Adicionando botões de download
        with open("massa_carga.csv", "rb") as f:
            st.download_button("📥 Baixar CSV", f, file_name="massa_carga.csv", mime="text/csv")

        with open("massa_carga.json", "rb") as f:
            st.download_button("📥 Baixar JSON", f, file_name="massa_carga.json", mime="application/json")


# 📤 Exportação de Relatório
elif menu == "Exportar Relatório":
    st.subheader("📑 Exportar Relatório de Casos de Teste")

    if st.button("📤 Exportar Relatório"):
        casos = gerar_casos_de_teste("Documento exemplo 1", "Documento exemplo 2")  # Exemplo para geração
        exportar_relatorio(casos)
        st.success("✅ Relatório exportado com sucesso!")
