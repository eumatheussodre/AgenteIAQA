# Funcionalidades/Ferramentas/api_tester_page.py

import streamlit as st
import requests
import json
from Funcionalidades.utils import exibir_e_baixar_json  # Importa a função auxiliar


def show_api_tester_page():
    """
    Renderiza a página completa para o Testador de API.
    """
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
                if 200 <= status_code < 300:
                    st.success(f"📡 Status: {status_code}")
                else:
                    st.error(f"📡 Status: {status_code}")

                st.info(
                    f"⏳ Tempo de Resposta: {resp.elapsed.total_seconds():.2f}s")
                st.subheader("📥 Resposta da API")
                try:
                    resposta_json = resp.json()
                    # Usa a função auxiliar importada
                    exibir_e_baixar_json(
                        "Corpo da Resposta (JSON)", resposta_json, "resposta_api.json")
                except json.JSONDecodeError:
                    st.text_area("Corpo da Resposta (Texto)",
                                 resp.text, height=200)

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao tentar conectar à API: {e}")
