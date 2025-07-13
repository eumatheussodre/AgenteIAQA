import streamlit as st
import requests
import json
import pandas as pd

# --- Módulos do Projeto ---
# Garanta que os módulos abaixo existem na sua estrutura de pastas (ex: Funcionalidades/Testes/Geradores/)
# para que a aplicação funcione corretamente.
try:
    from Funcionalidades.Testes.Geradores.generator_Date import gerar_massa_de_dados
    from Funcionalidades.Testes.Geradores.generator_Casos import gerar_casos_de_teste
    from Funcionalidades.Testes.Geradores.generator_Bank import gerar_massa_bancaria
    from Funcionalidades.Testes.Geradores.generator_Report import exportar_relatorio
except ImportError:
    st.error("ERRO: Não foi possível encontrar os módulos de funcionalidades. Verifique a estrutura do seu projeto.")
    st.stop()


# --- Funções Auxiliares (Reutilizáveis) ---

def exibir_e_baixar_json(titulo, dados_json, nome_arquivo):
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


def exibir_e_baixar_csv(titulo, dataframe, nome_arquivo):
    """Exibe um título, uma tabela de dados e um botão de download para CSV."""
    st.subheader(titulo)
    # Mostra apenas as primeiras linhas para performance
    st.dataframe(dataframe.head())
    csv_string = dataframe.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv_string,
        file_name=nome_arquivo,
        mime="text/csv"
    )

# --- Inicialização do Estado da Sessão ---


def inicializar_estado():
    """Define os valores iniciais para o st.session_state se não existirem."""
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Gerador de Dados"
    if "casos_de_teste_gerados" not in st.session_state:
        st.session_state.casos_de_teste_gerados = []
    if "api_headers" not in st.session_state:
        st.session_state.api_headers = {}


inicializar_estado()

# --- Barra Lateral (Sidebar) ---

with st.sidebar:
    st.image(
        "https://d1my6w132otbna.cloudfront.net/pub/media/wysiwyg/TGI/tgi-logo-300.png", width=150)
    st.header("📌 Menu Principal")

    paginas_menu = [
        "Gerar Cenários de Teste",
        "Gerador de Dados",
        "Gerador de Massa Bancária",
        "Gerador de Testes de Carga",
        "Testar API",
        "Exportar Relatório"
    ]
    st.session_state.pagina = st.radio(
        "Selecione uma funcionalidade:",
        paginas_menu,
        key="menu_principal"
    )

# Título da Página Dinâmico
st.title(f"🧪 AgenteIA Engine – TGI | {st.session_state.pagina}")


# --- Lógica das Páginas ---

if st.session_state.pagina == "Gerar Cenários de Teste":
    st.subheader("📁 Upload de Documentos")
    st.info("Envie os documentos de desenvolvimento e especificação para gerar os casos de teste.")

    uploaded_dev = st.file_uploader("Documento do Desenvolvedor", type=[
                                    "pdf", "txt", "md", "docx"])
    uploaded_spec = st.file_uploader("Especificação Funcional", type=[
                                     "pdf", "txt", "md", "docx"])

    if uploaded_dev and uploaded_spec:
        st.success("✅ Documentos recebidos!")
        if st.button("🧠 Gerar Casos de Teste", type="primary"):
            with st.spinner("Analisando documentos e gerando casos..."):
                texto_dev = processar_arquivo(uploaded_dev)
                texto_spec = processar_arquivo(uploaded_spec)
                casos = gerar_casos_de_teste(texto_dev, texto_spec)
                st.session_state.casos_de_teste_gerados = casos

            if casos:
                st.subheader("✅ Casos de Teste Gerados")
                for i, caso in enumerate(casos, 1):
                    st.markdown(f"**Caso {i}:**\n```\n{caso}\n```")
                txt_buffer = "\n\n".join(casos)
                st.download_button(
                    "⬇️ Baixar Casos (.txt)", data=txt_buffer, file_name="casos_de_teste.txt")
            else:
                st.warning(
                    "⚠️ Nenhum caso de teste foi gerado a partir dos documentos.")

elif st.session_state.pagina == "Gerador de Dados":
    st.subheader("⚙️ Gerador de Massa de Dados para QA")
    campos_disponiveis = ["nome", "email", "cpf", "cnpj",
                          "telefone", "endereco", "data_nascimento"]
    campos_selecionados = st.multiselect(
        "Campos a serem gerados", campos_disponiveis, default=campos_disponiveis)
    quantidade = st.slider("Quantidade de registros", 1, 100, 10)

    if st.button("📊 Gerar Dados", type="primary"):
        if not campos_selecionados:
            st.error("Por favor, selecione pelo menos um campo para gerar.")
        else:
            massa_dados = gerar_massa_de_dados(quantidade, campos_selecionados)
            exibir_e_baixar_json(
                f"📄 {quantidade} Registros Gerados", massa_dados, "massa_dados.json")

elif st.session_state.pagina == "Gerador de Massa Bancária":
    st.subheader("🏦 Gerador de Massa de Dados Bancários")
    quantidade = st.slider("Quantidade de contas bancárias", 1, 100, 10)
    if st.button("💳 Gerar Dados Bancários", type="primary"):
        massa_bancaria = gerar_massa_bancaria(quantidade)
        exibir_e_baixar_json(
            f"📄 {quantidade} Contas Geradas", massa_bancaria, "massa_bancaria.json")

elif st.session_state.pagina == "Gerador de Testes de Carga":
    st.subheader("⚡ Gerador de Testes de Carga")
    st.info("Gere um grande volume de dados para testes de performance e carga.")
    quantidade = st.number_input(
        "Quantidade de registros", min_value=1000, max_value=200000, value=10000, step=1000)

    if st.button("🔥 Gerar Dados de Carga", type="primary"):
        with st.spinner(f"Gerando {quantidade} registros..."):
            dados_carga = gerar_massa_de_dados(
                quantidade, ["nome", "email", "cpf", "id_transacao", "valor"])
            df_carga = pd.DataFrame(dados_carga)
        st.success(f"✅ {quantidade} registros de carga gerados!")
        exibir_e_baixar_csv("Amostra dos Dados (CSV)",
                            df_carga, "massa_carga.csv")
        exibir_e_baixar_json("Dados Completos (JSON)",
                             dados_carga, "massa_carga.json")

elif st.session_state.pagina == "Testar API":
    st.subheader("🌐 Testador de API")
    url = st.text_input(
        "🔗 URL da API", placeholder="https://api.example.com/data")
    metodo = st.selectbox("Método HTTP", ["GET", "POST", "PUT", "DELETE"])

    st.markdown("##### **Cabeçalhos (Headers)**")
    col1, col2, col3 = st.columns([3, 3, 1])
    header_key = col1.text_input(
        "Chave", key="h_key", label_visibility="collapsed", placeholder="Chave")
    header_value = col2.text_input(
        "Valor", key="h_val", label_visibility="collapsed", placeholder="Valor")
    if col3.button("Adicionar", key="add_header"):
        if header_key and header_value:
            st.session_state.api_headers[header_key] = header_value
            st.rerun()
        else:
            st.warning("Preencha a chave e o valor do cabeçalho.")

    if st.session_state.api_headers:
        st.write("Cabeçalhos atuais:")
        for key, value in list(st.session_state.api_headers.items()):
            col_k, col_v, col_del = st.columns([3, 3, 1])
            col_k.write(f"`{key}`")
            col_v.write(f"`{value}`")
            if col_del.button(f"❌", key=f"del_{key}"):
                del st.session_state.api_headers[key]
                st.rerun()

    payload_str = ""
    if metodo in ["POST", "PUT"]:
        payload_str = st.text_area("📤 Corpo da Requisição (JSON)", height=150)

    if st.button("🚀 Enviar Requisição", type="primary"):
        if not url.startswith(("http://", "https://")):
            st.error("URL inválida. Deve começar com http:// ou https://")
        else:
            payload = None
            if payload_str:
                try:
                    payload = json.loads(payload_str)
                except json.JSONDecodeError as e:
                    st.error(
                        f"Erro no formato JSON do corpo da requisição: {e}")
                    st.stop()
            try:
                with st.spinner("Enviando requisição..."):
                    resp = getattr(requests, metodo.lower())(
                        url, json=payload, headers=st.session_state.api_headers, timeout=10
                    )
                status_code = resp.status_code
                st.success(f"📡 Status: {status_code}") if 200 <= status_code < 300 else st.error(
                    f"📡 Status: {status_code}")
                st.info(
                    f"⏳ Tempo de Resposta: {resp.elapsed.total_seconds():.2f}s")
                st.subheader("📥 Resposta da API")
                try:
                    resposta_json = resp.json()
                    exibir_e_baixar_json(
                        "Corpo da Resposta (JSON)", resposta_json, "resposta_api.json")
                except json.JSONDecodeError:
                    st.text_area("Corpo da Resposta (Texto)",
                                 resp.text, height=200)
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao tentar conectar à API: {e}")

elif st.session_state.pagina == "Exportar Relatório":
    st.subheader("📑 Exportar Relatório de Casos de Teste")
    casos_para_exportar = st.session_state.casos_de_teste_gerados
    if not casos_para_exportar:
        st.warning("⚠️ Nenhum caso de teste foi gerado ainda.")
        st.info(
            "Vá para a página 'Gerar Cenários de Teste' para criar os casos primeiro.")
    else:
        st.success(
            f"✅ {len(casos_para_exportar)} casos de teste prontos para serem exportados.")
        st.markdown("Pré-visualização dos casos:")
        for caso in casos_para_exportar[:3]:
            st.markdown(f"```\n{caso}\n```")
        if st.button("📤 Exportar Relatório Agora", type="primary"):
            exportar_relatorio(casos_para_exportar)
