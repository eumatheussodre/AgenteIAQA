# Funcionalidades/Testes/Geradores/generator_Casos.py

import os
import json
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# --- Constantes e Configuração da API do Google ---
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
API_KEY = os.getenv("GOOGLE_API_KEY")


def construir_prompt_login() -> str:
    """Constrói o prompt detalhado para gerar testware de login."""

    # O seu prompt, agora integrado diretamente no código.
    # Adicionamos instruções explícitas para a IA retornar um JSON.
    prompt = """
    Aja como um especialista em Quality Assurance. Utilize questionamento socrático internamente para desenvolver os seguintes testwares para a funcionalidade de Login de um sistema. A tela de login contém apenas os campos "username", "password" e um botão de "login". O tipo de teste a ser executado é apenas funcional, focado na norma ISO 25010.

    **Sua resposta DEVE ser um único objeto JSON válido, contendo duas chaves principais: "cenarios_storytelling" e "casos_de_teste_tabela".**

    1.  **Para a chave "cenarios_storytelling":**
        * Crie uma lista de strings. Cada string deve ser o título de um cenário de teste utilizando storytelling.
        * O título deve gerar empatia e expor um objetivo do usuário.
        * Exemplo de um bom título: "Acesso rápido à conta por um gestor de projetos antes de uma reunião importante."

    2.  **Para a chave "casos_de_teste_tabela":**
        * Crie uma ÚNICA STRING contendo uma tabela de decisão em formato Markdown.
        * A tabela não pode estar quebrada ou mal formatada.
        * Organize a tabela com as seguintes seções e técnicas de teste, nesta ordem:
            * 🟢 **Testes Positivos (Caminho Feliz):** Username e password válidos.
            * 🟠 **Testes Negativos (Inputs Válidos):** Combinações de username e password que existem mas não correspondem, ou contas bloqueadas.
            * 🔴 **Testes Negativos (Inputs Inválidos):** Use Partição de Equivalência e Análise de Valor Limite. Teste cada variável inválida separadamente (username inválido, senha inválida) e depois todas juntas.
            * 💥 **Testes Destrutivos:** Inputs inesperados, como injeção de SQL simples, scripts, ou caracteres especiais.

    **Exemplo do formato JSON esperado:**
    {
      "cenarios_storytelling": [
        "Título do cenário 1...",
        "Título do cenário 2..."
      ],
      "casos_de_teste_tabela": "| Técnica | ID do Teste | Condição (Username) | Condição (Password) | Ação | Resultado Esperado |\\n|---|---|---|---|---|---|\\n| 🟢 Positivo | CTP-001 | Usuário Válido | Senha Válida | Clicar em Login | Login bem-sucedido. |\\n..."
    }
    """
    return prompt


def gerar_casos_de_teste(texto_requisitos_dev: str, texto_requisitos_spec: str) -> list[str]:
    """
    Gera casos de teste usando a API do Google Gemini, solicitando e processando uma resposta JSON.
    Os argumentos texto_requisitos_* são mantidos para compatibilidade com a interface, mas o prompt principal é fixo.
    """
    if not API_KEY:
        return ["⚠️ Erro: Chave da API do Google (GOOGLE_API_KEY) não encontrada."]

    # Usa a nova função para construir o prompt específico de login
    prompt_texto = construir_prompt_login()

    url_com_chave = f"{API_URL}?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt_texto}]}],
        # Configurações para forçar a saída em formato JSON
        "generationConfig": {
            "response_mime_type": "application/json",
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(
            url_com_chave, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        resultado_json = response.json()

        # Extrai o conteúdo do JSON gerado pela IA
        conteudo_gerado = resultado_json['candidates'][0]['content']['parts'][0]['text']
        dados = json.loads(conteudo_gerado)

        # Agora, processamos o JSON recebido para formatar a saída para o Streamlit
        saida_formatada = []

        # Adiciona o título da primeira seção
        saida_formatada.append("### 🎭 Cenários de Teste (Storytelling)")
        cenarios = dados.get("cenarios_storytelling", [])
        if cenarios:
            saida_formatada.extend([f"- {cenario}" for escenario in cenarios])
        else:
            saida_formatada.append(
                "Nenhum cenário de storytelling foi gerado.")

        # Adiciona um separador e o título da segunda seção
        saida_formatada.append(
            "\n---\n### 📊 Casos de Teste (Tabela de Decisão)")
        tabela_markdown = dados.get(
            "casos_de_teste_tabela", "A tabela de casos de teste não foi gerada.")

        # Adiciona a tabela inteira como um único item, para garantir que não seja quebrada
        saida_formatada.append(tabela_markdown)

        return saida_formatada

    except requests.RequestException as e:
        detalhes = f"Detalhes: {e.response.text}" if e.response else "Sem detalhes adicionais."
        return [f"❌ Erro na requisição à API: {e}. {detalhes}"]
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return [f"❌ Erro ao processar a resposta da API. A estrutura do JSON pode ser inválida. Detalhe: {e}"]
