import streamlit as st
import requests
import json
import os
import importlib

# Importando os módulos necessários
from Funcionalidades.Testes.Geradores.generator_Date import gerar_massa_de_dados
from Funcionalidades.Testes.Geradores.generator_Casos import gerar_casos_de_teste
from Funcionalidades.Testes.Geradores.generator_Bank import *
from Funcionalidades.Testes.Geradores.generator_Report import *
from Funcionalidades.Testes.Geradores.generator_Stress import *

def salvar_csv(filename, quantidade):
    raise NotImplementedError

def salvar_json(filename, quantidade):
    raise NotImplementedError

# Inicializa a página
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# Menu lateral
with st.sidebar.expander("📌 Geradores de Dados", expanded=False):
    opcao_geradores = st.radio(
        "Selecione uma opção:",
        ["Gerador de Dados", "Gerador de Massa Bancária", "Gerador de Testes de Carga", "Gerar Casos de Teste"],
        key="menu_geradores"
    )
    st.session_state.pagina = opcao_geradores

with st.sidebar.expander("📌 Testes", expanded=False):
    opcao_testes = st.radio(
        "Selecione uma opção:",
        ["Testar API"],
        key="menu_testes"
    )
    st.session_state.pagina = opcao_testes

with st.sidebar.expander("📌 Relatórios", expanded=False):
    opcao_relatorios = st.radio(
        "Selecione uma opção:",
        ["Exportar Relatório"],
        key="menu_relatorios"
    )
    st.session_state.pagina = opcao_relatorios


CAMPOS_DISPONIVEIS = [
    "nome", "email", "cpf", "cnpj", "telefone", "endereco", "data_nascimento"
]

if opcao_geradores == "Gerar Casos de Teste":
    st.subheader("📁 Upload de Documentos")
    st.markdown("Faça upload dos documentos para gerar os casos de teste.")

    uploaded_dev = st.file_uploader("Documento do Desenvolvedor", type=["pdf", "xlsx", "png", "jpg"])
    uploaded_spec = st.file_uploader("Especificação Funcional", type=["pdf", "xlsx", "png", "jpg"])

    if uploaded_dev and uploaded_spec:
        st.success("✅ Documentos enviados!")
        texto_dev = processar_arquivo(uploaded_dev)
        texto_spec = processar_arquivo(uploaded_spec)

        if st.button("🧠 Gerar Casos de Teste"):
            casos = gerar_casos_de_teste(texto_dev, texto_spec) or []
            if casos:
                st.subheader("✅ Casos de Teste Gerados")
                for i, caso in enumerate(casos, 1):
                    st.markdown(f"**Caso {i}:**\n```\n{caso}\n```")
                import io
                txt_buffer = io.StringIO()
                txt_buffer.write("\n\n".join(casos))
                txt_buffer.seek(0)
                st.download_button("⬇️ Baixar Casos (.txt)", data=txt_buffer.getvalue(), file_name="casos_de_teste.txt", mime="text/plain")
            else:
                st.warning("⚠️ Nenhum caso de teste foi gerado.")
    else:
        st.info("Envie ambos os documentos para continuar.")

elif opcao_geradores == "Gerador de Dados":
    st.subheader("⚙️ Gerador de Massa de Dados para QA")
    quantidade = st.slider("Quantidade de registros", 1, 50, 10)
    campos = st.multiselect("Campos a serem gerados", CAMPOS_DISPONIVEIS, default=CAMPOS_DISPONIVEIS)
    if st.button("📊 Gerar Dados"):
        massa_dados = gerar_massa_de_dados(quantidade, campos)
        st.subheader(f"📄 {quantidade} Registros Gerados")
        st.json(massa_dados)

        import io, csv
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=massa_dados[0].keys())
        writer.writeheader()
        writer.writerows(massa_dados)
        st.download_button("⬇️ Baixar CSV", data=csv_buffer.getvalue(), file_name="massa_dados.csv", mime="text/csv")

        json_buffer = io.StringIO()
        json.dump(massa_dados, json_buffer, ensure_ascii=False, indent=4)
        st.download_button("⬇️ Baixar JSON", data=json_buffer.getvalue(), file_name="massa_dados.json", mime="application/json")

elif opcao_geradores == "Gerador de Massa Bancária":
    st.subheader("🏦 Gerador de Massa de Dados Bancários")
    quantidade = st.slider("Quantidade de contas bancárias", 1, 50, 10)
    if st.button("💳 Gerar Dados Bancários"):
        massa_bancaria = gerar_massa_bancaria(quantidade)
        st.subheader(f"📄 {quantidade} Contas Geradas")
        for dado in massa_bancaria:
            st.write(dado)

        import io
        json_bytes = io.BytesIO()
        json_bytes.write(json.dumps(massa_bancaria, ensure_ascii=False, indent=4).encode('utf-8'))
        json_bytes.seek(0)
        st.download_button("⬇️ Baixar JSON", data=json_bytes, file_name="massa_bancaria.json", mime="application/json")

elif opcao_geradores == "Gerador de Testes de Carga":
    st.subheader("⚡ Gerador de Testes de Carga")
    quantidade = st.slider("Quantidade de registros", 1000, 100000, 10000, step=1000)
    if st.button("🔥 Gerar Dados de Carga"):
        salvar_csv("massa_carga.csv", quantidade)
        salvar_json("massa_carga.json", quantidade)
        st.success(f"✅ {quantidade} registros gerados com sucesso!")

elif opcao_relatorios == "Exportar Relatório":
    st.subheader("📑 Exportar Relatório de Casos de Teste")
    if st.button("📤 Exportar Relatório"):
        casos = gerar_casos_de_teste("Documento exemplo 1", "Documento exemplo 2")
        exportar_relatorio(casos)
        st.success("✅ Relatório exportado com sucesso!")

elif opcao_testes == "Testar API":
    st.subheader("🌐 Testador de API")
    url = st.text_input("🔗 URL da API", "")
    metodo = st.selectbox("Método HTTP", ["GET", "POST", "PUT", "DELETE"])
    payload = None
    headers = {}

    if metodo in ["POST", "PUT"]:
        payload_str = st.text_area("📤 Payload JSON (opcional)", "")
        if payload_str.strip():
            try:
                payload = json.loads(payload_str)
            except Exception as e:
                st.error(f"Payload JSON inválido: {e}")

    header_key = st.text_input("Header Key", key="header_key")
    header_value = st.text_input("Header Value", key="header_value")
    if header_key and header_value:
        headers[header_key] = header_value

    if st.button("🚀 Enviar Requisição"):
        if not url.startswith("http://") and not url.startswith("https://"):
            st.error("URL inválida! Deve começar com http:// ou https://")
        else:
            try:
                if metodo == "GET":
                    resposta = requests.get(url, headers=headers, timeout=5)
                elif metodo == "POST":
                    resposta = requests.post(url, json=payload, headers=headers, timeout=5)
                elif metodo == "PUT":
                    resposta = requests.put(url, json=payload, headers=headers, timeout=5)
                elif metodo == "DELETE":
                    resposta = requests.delete(url, headers=headers, timeout=5)
                else:
                    st.error("Método HTTP inválido!")
                    resposta = None

                if resposta:
                    st.write(f"📡 Status HTTP: {resposta.status_code}")
                    st.write(f"⏳ Tempo de resposta: {resposta.elapsed.total_seconds()}s")
                    st.write("📦 Headers da resposta:", dict(resposta.headers))
                    try:
                        resposta_json = resposta.json()
                        st.json(resposta_json)
                        resposta_bytes = json.dumps(resposta_json, ensure_ascii=False, indent=4).encode("utf-8")
                        st.download_button("⬇️ Baixar resposta JSON", data=resposta_bytes, file_name="resposta.json", mime="application/json")
                    except Exception:
                        st.text_area("📥 Resposta da API (texto)", resposta.text, height=200)
                        st.download_button("⬇️ Baixar resposta TXT", data=resposta.text, file_name="resposta.txt", mime="text/plain")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao executar requisição: {e}")
