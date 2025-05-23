import streamlit as st
import requests
import json
import io

# Importando os módulos necessários
from Funcionalidades.Testes.Geradores.generator_Date import gerar_massa_de_dados
from Funcionalidades.Testes.Geradores.generator_Casos import gerar_casos_de_teste
from Funcionalidades.Testes.Geradores.generator_Bank import gerar_massa_bancaria
from Funcionalidades.Testes.Geradores.generator_Report import exportar_relatorio
from Funcionalidades.Testes.Geradores.generator_Stress import *
from Funcionalidades.utils import *

# Funções de salvamento de carga (implementar conforme necessidade)
def salvar_csv(filename, quantidade):
    raise NotImplementedError

def salvar_json(filename, quantidade):
    raise NotImplementedError

# Inicializa a página
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# Menu unificado
with st.sidebar.expander("📌 Menu", expanded=False):
    opcao = st.radio(
        "Selecione uma funcionalidade:",
        [
            "Gerador de Dados",
            "Gerador de Massa Bancária",
            "Gerador de Testes de Carga",
            "Gerar Casos de Teste",
            "Testar API"
        ],
        key="menu_unificado"
    )
    st.session_state.pagina = opcao

# Exportar Relatório como opção independente
if st.sidebar.button("📤 Exportar Relatório", key="exportar_relatorio"):
    st.session_state.pagina = "Exportar Relatório"

# Cabeçalho
st.title(f"🧪 AgenteIA Engine – TGI | {st.session_state.pagina}")

# Campos disponíveis para geração de dados
CAMPOS_DISPONIVEIS = [
    "nome", "email", "cpf", "cnpj", "telefone", "endereco", "data_nascimento"
]

pagina = st.session_state.pagina

# Conteúdo das páginas
if pagina == "Gerar Casos de Teste":
    st.subheader("📁 Upload de Documentos")
    uploaded_dev = st.file_uploader("Documento do Desenvolvedor", type=["pdf", "xlsx", "png", "jpg"])
    uploaded_spec = st.file_uploader("Especificação Funcional", type=["pdf", "xlsx", "png", "jpg"])

    if uploaded_dev and uploaded_spec:
        st.success("✅ Documentos recebidos!")
        texto_dev = processar_arquivo(uploaded_dev)
        texto_spec = processar_arquivo(uploaded_spec)
        if st.button("🧠 Gerar Casos de Teste"):
            casos = gerar_casos_de_teste(texto_dev, texto_spec) or []
            if casos:
                st.subheader("✅ Casos de Teste Gerados")
                for i, caso in enumerate(casos, 1):
                    st.markdown(f"**Caso {i}:**\n```\n{caso}\n```")
                txt_buffer = io.StringIO()
                txt_buffer.write("\n\n".join(casos))
                st.download_button("⬇️ Baixar Casos (.txt)", data=txt_buffer.getvalue(), file_name="casos_de_teste.txt")
            else:
                st.warning("⚠️ Nenhum caso gerado.")
    else:
        st.info("Envie ambos os documentos para continuar.")
elif pagina == "Gerador de Dados":
    st.subheader("⚙️ Gerador de Massa de Dados para QA")
    quantidade = st.slider("Quantidade de registros", 1, 50, 10)
    campos = st.multiselect("Campos a serem gerados", CAMPOS_DISPONIVEIS, default=CAMPOS_DISPONIVEIS)
    if st.button("📊 Gerar Dados"):
        massa_dados = gerar_massa_de_dados(quantidade, campos)
        st.subheader(f"📄 {quantidade} Registros Gerados")
        st.json(massa_dados)

        csv_buffer = io.StringIO()
        writer = json.dumps(massa_dados, ensure_ascii=False, indent=4)
        st.download_button("⬇️ Baixar JSON", data=writer, file_name="massa_dados.json")
elif pagina == "Gerador de Massa Bancária":
    st.subheader("🏦 Gerador de Massa de Dados Bancários")
    quantidade = st.slider("Quantidade de contas bancárias", 1, 50, 10)
    if st.button("💳 Gerar Dados Bancários"):
        massa_bancaria = gerar_massa_bancaria(quantidade)
        st.subheader(f"📄 {quantidade} Contas Geradas")
        st.json(massa_bancaria)

        json_bytes = json.dumps(massa_bancaria, ensure_ascii=False, indent=4).encode('utf-8')
        st.download_button("⬇️ Baixar JSON", data=json_bytes, file_name="massa_bancaria.json")
elif pagina == "Gerador de Testes de Carga":
    st.subheader("⚡ Gerador de Testes de Carga")
    quantidade = st.slider("Quantidade de registros", 1000, 100000, 10000, step=1000)
    if st.button("🔥 Gerar Dados de Carga"):
        salvar_csv("massa_carga.csv", quantidade)
        salvar_json("massa_carga.json", quantidade)
        st.success(f"✅ {quantidade} registros de carga gerados!")
elif pagina == "Testar API":
    st.subheader("🌐 Testador de API | v.01")
    url = st.text_input("🔗 URL da API")
    metodo = st.selectbox("Método HTTP", ["GET", "POST", "PUT", "DELETE"])
    payload = None
    headers = {}

    if metodo in ["POST", "PUT"]:
        payload_str = st.text_area("📤 Payload JSON (opcional)")
        if payload_str:
            try:
                payload = json.loads(payload_str)
            except Exception as e:
                st.error(f"Payload inválido: {e}")

    key = st.text_input("Header Key")
    value = st.text_input("Header Value")
    if key and value:
        headers[key] = value

    if st.button("🚀 Enviar Requisição"):
        if not url.startswith(("http://", "https://")):
            st.error("URL deve começar com http:// ou https://")
        else:
            try:
                resp = getattr(requests, metodo.lower())(url, json=payload, headers=headers, timeout=5)
                st.write(f"📡 Status: {resp.status_code}")
                st.write(f"⏳ Tempo: {resp.elapsed.total_seconds()}s")
                try:
                    data = resp.json()
                    st.json(data)
                    st.download_button("⬇️ Baixar JSON", data=json.dumps(data, indent=4), file_name="resposta.json")
                except:
                    st.text_area("📥 Resposta", resp.text, height=200)
            except Exception as e:
                st.error(f"Erro: {e}")
elif pagina == "Exportar Relatório":
    st.subheader("📑 Exportar Relatório de Casos de Teste")
    if st.button("📤 Exportar Relatório"):
        casos = gerar_casos_de_teste("doc1", "doc2")
        exportar_relatorio(casos)
        st.success("✅ Relatório exportado!")
