import streamlit as st
from test_generator import gerar_casos_de_teste
from file_processor import processar_arquivo
from report_generator import exportar_relatorio
from data_generator import gerar_massa_de_dados
from bank_generator import gerar_massa_bancaria 
from load_generator import salvar_csv, salvar_json


st.set_page_config(page_title="Agente IA - [QA] - Prototipo - i4Pro", layout="wide")
st.title("🧪 Agente IA - Prototipo [QA] - i4Pro")

# 🏠 Menu lateral atualizado com nova opção
menu = st.sidebar.radio("📌 Selecione uma função:", 
[
    "Gerar Casos de Teste",
    "Gerador de Dados/Massa",
    "Gerador de Massa Bancária",
    "Gerador de Testes de Carga",  # ✅ Adicionado ao menu!
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
elif menu == "Gerador de Dados/Massa":
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
elif menu == "Gerador Carga de Testes":
    st.subheader("⚡ Gerador de Testes de Carga")

    quantidade = st.slider("Quantidade de registros", min_value=1000, max_value=100000, value=10000)

    if st.button("🔥 Gerar Dados para Testes de Carga"):
        salvar_csv("massa_carga.csv", quantidade)
        salvar_json("massa_carga.json", quantidade)
        
        st.success(f"✅ {quantidade} registros gerados! Arquivos `massa_carga.csv` e `massa_carga.json` criados!")

# 📤 Exportação de Relatório
elif menu == "Exportar Relatório":
    st.subheader("📑 Exportar Relatório de Casos de Teste")

    if st.button("📤 Exportar Relatório"):
        casos = gerar_casos_de_teste("Documento exemplo 1", "Documento exemplo 2")  # Exemplo para geração
        exportar_relatorio(casos)
        st.success("✅ Relatório exportado com sucesso!")
