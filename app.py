import streamlit as st
import pandas as pd

# --- Módulos do Projeto ---
# Importa as funções de cada módulo/página.
# O bloco try-except ajuda a garantir que todos os ficheiros necessários existem.
try:
    # Funções geradoras a partir do pacote 'Geradores'
    from Funcionalidades.Testes.Geradores import (
        gerar_massa_de_dados,
        gerar_casos_de_teste,
        gerar_massa_bancaria,
        exportar_relatorio
    )
    # Funções de utilidade (processamento de ficheiros, botões de download, etc.)
    from Funcionalidades.utils import (
        processar_arquivo,
        exibir_e_baixar_json,
        exibir_e_baixar_csv
    )
    # A função que renderiza a página de teste de API
    from Funcionalidades.Ferramentas.api_tester_page import show_api_tester_page
except ImportError as e:
    # Se uma importação falhar, exibe uma mensagem de erro clara
    st.error(
        f"ERRO: Não foi possível importar um módulo essencial: '{e.name}'. "
        "Verifique se a estrutura de pastas e os ficheiros do projeto estão corretos."
    )
    st.stop()  # Interrompe a execução se um módulo crítico estiver em falta

# --- Inicialização do Estado da Sessão ---


def inicializar_estado():
    """Define os valores iniciais para o st.session_state se ainda não existirem."""
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Gerar Cenários de Teste"
    if "casos_de_teste_gerados" not in st.session_state:
        st.session_state.casos_de_teste_gerados = []
    if "api_headers" not in st.session_state:
        # Garante que os headers da API sejam inicializados como um dicionário
        st.session_state.api_headers = {}


# Chama a função de inicialização no início de cada execução
inicializar_estado()

# --- Barra Lateral de Navegação (Sidebar) ---
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

    # O st.radio controla qual página é exibida
    st.session_state.pagina = st.radio(
        "Selecione uma funcionalidade:",
        paginas_menu,
        key="menu_principal"
    )

# --- Título Principal da Página (Dinâmico) ---
st.title(f"🧪 AgenteIA Engine – TGI | {st.session_state.pagina}")

# --- Roteador de Páginas ---
# Este bloco 'if/elif' direciona para a lógica da página selecionada no menu.
pagina_atual = st.session_state.pagina

if pagina_atual == "Gerar Cenários de Teste":
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

elif pagina_atual == "Gerador de Dados":
    st.subheader("⚙️ Gerador de Massa de Dados para QA")
    campos_disponiveis = ["nome", "email", "cpf", "cnpj",
                          "telefone", "endereco", "data_nascimento", "empresa"]
    campos_selecionados = st.multiselect(
        "Campos a serem gerados", campos_disponiveis, default=["nome", "email", "cpf"])
    quantidade = st.slider("Quantidade de registros", 1, 100, 10)

    if st.button("📊 Gerar Dados", type="primary"):
        if not campos_selecionados:
            st.error("Por favor, selecione pelo menos um campo para gerar.")
        else:
            massa_dados = gerar_massa_de_dados(quantidade, campos_selecionados)
            exibir_e_baixar_json(
                f"📄 {quantidade} Registros Gerados", massa_dados, "massa_dados.json")

elif pagina_atual == "Gerador de Massa Bancária":
    st.subheader("🏦 Gerador de Massa de Dados Bancários")
    quantidade = st.slider("Quantidade de contas bancárias", 1, 100, 10)
    permitir_negativo = st.checkbox("Permitir saldo negativo")

    if st.button("💳 Gerar Dados Bancários", type="primary"):
        massa_bancaria = gerar_massa_bancaria(quantidade, permitir_negativo)
        exibir_e_baixar_json(
            f"📄 {quantidade} Contas Geradas", massa_bancaria, "massa_bancaria.json")

elif pagina_atual == "Gerador de Testes de Carga":
    st.subheader("⚡ Gerador de Testes de Carga")
    st.info("Gere um grande volume de dados para testes de performance e carga.")
    quantidade = st.number_input(
        "Quantidade de registros", min_value=1000, max_value=200000, value=10000, step=1000)

    if st.button("🔥 Gerar Dados de Carga", type="primary"):
        with st.spinner(f"Gerando {quantidade} registros..."):
            dados_carga = gerar_massa_de_dados(
                quantidade, ["nome", "email", "cpf", "empresa"])
            df_carga = pd.DataFrame(dados_carga)
        st.success(f"✅ {quantidade} registros de carga gerados!")
        exibir_e_baixar_csv("Amostra dos Dados (CSV)",
                            df_carga, "massa_carga.csv")
        exibir_e_baixar_json("Dados Completos (JSON)",
                             dados_carga, "massa_carga.json")

elif pagina_atual == "Testar API":
    # A lógica desta página foi movida para seu próprio módulo para organização.
    # O app.py apenas chama a função que renderiza a página.
    show_api_tester_page()

elif pagina_atual == "Exportar Relatório":
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
        # Mostra os 3 primeiros como exemplo
        for caso in casos_para_exportar[:3]:
            st.markdown(f"```\n{caso}\n```")

        nome_relatorio = st.text_input(
            "Nome base para os relatórios:", value="relatorio_de_testes")

        if st.button("📤 Exportar Relatórios Agora", type="primary"):
            with st.spinner("Gerando relatórios..."):
                exportar_relatorio(casos_para_exportar, nome_relatorio)
            st.success(
                f"Relatórios gerados com o nome base '{nome_relatorio}'!")
