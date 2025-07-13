# generator_Casos.py

import os
import json
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# --- Constantes ---
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
# Carrega o token de forma segura a partir das variáveis de ambiente
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


def gerar_casos_de_teste(texto_requisitos_dev: str, texto_requisitos_spec: str) -> list[str]:
    """
    Gera casos de teste em formato de texto a partir de documentos de requisitos,
    solicitando uma resposta JSON estruturada da API de IA.
    """
    if not API_TOKEN:
        print("⚠️ Erro: Token da API (HUGGINGFACE_API_TOKEN) não encontrado nas variáveis de ambiente.")
        return []

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Prompt instruindo a IA a retornar um JSON estruturado.
    # Isto é muito mais robusto do que processar texto livre.
    prompt = f"""
    Quero que você desenvolva os seguintes testwares para a funcionalidade de Login.
Utilize questionamento socrático em todo o processo, mas não precisa mostrar as perguntas. Mostre apenas se eu pedir.

Login: A tela de login contém apenas campo de username, password e botão de login.

Tipo de teste a ser executado: Apenas funcional - ISO 25010.
Artefatos:
    Cenário de teste utilizando storytelling
        Forma: 
            Aqui não é para contar uma história, é para montar um caso de teste que considere a realidade do usuário final, guiando o QA para pensar e agir como o usuário final.
            Exiba apenas o titulo do cenário de teste. 
            Mostre a história apenas se eu pedir.
            Os cenário devem ser reestritos ao contexto de utilização da funcionalidade que estamos testando.
            O nome deve: 
                Gerar empatia no leitor.
                Expor um possível propósito/objetivo pelo qual o usuário vai utilizar a funcionalidade/serviço.
        Exemplo:
            Cenário errado: Registro de um voo
            Cenário certo: Agendamento de voo por um casal em viajem de lua de mel

    Casos de teste utilizando técnicas de teste
            Construa uma tabela de decisão utilizando as técnicas:
                Teste positivo/negativo/destrutivo
                Análise do valor limite
                Partição de equivalência
                Organização da tabela:
                    🟢 Testes positivos (caminho feliz)
                    🟢 Testes positivos com parâmetros opcionais
                    🟠 Testes negativos com inputs validos
                    🔴 Testes negativos com inputs inválidos
                    💥 Testes destrutivos

Reforço:
1. Construa os cenários onde são testados valores inválidos para cada variável e ao final mais um cenário para todas as variáveis inválidas;
    Exemplo:
        Cenário 1: usuário = valido | senha = valida
        Cenário 2: usuário = invalido | senha = valida
        Cenário 3: usuário = valido | senha = invalida
        Cenário 4: usuário = valido | senha = invalida
2. Considere correlações entre as variáveis;
3. A tabela exibida não pode ficar desformatada;
4. Aprenda e reflita sobre os princípios das técnicas e estratégias de teste solicitadas."""

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 1024, "temperature": 0.5},
    }

    try:
        response = requests.post(
            API_URL, headers=headers, json=payload, timeout=90)
        response.raise_for_status()  # Lança uma exceção para status de erro (4xx ou 5xx)

        # Extrai o texto gerado pela IA
        resultado_bruto = response.json()
        texto_gerado = resultado_bruto[0]['generated_text']

        # A IA pode retornar o JSON dentro de um bloco de código, então extraímos apenas o JSON
        json_str = texto_gerado[texto_gerado.find(
            '['):texto_gerado.rfind(']')+1]

        # Converte a string JSON numa lista de dicionários Python
        casos_json = json.loads(json_str)

        # Formata a lista de dicionários para a lista de strings esperada
        casos_formatados = []
        for caso in casos_json:
            etapas_str = "\n".join(
                [f"- {etapa}" for etapa in caso.get("etapas", [])])
            caso_str = (
                f"ID: {caso.get('id', 'N/A')}\n"
                f"Descrição: {caso.get('descricao', 'N/A')}\n"
                f"{etapas_str}\n"
                f"Resultado Esperado: {caso.get('resultado_esperado', 'N/A')}"
            )
            casos_formatados.append(caso_str)

        return casos_formatados

    except requests.RequestException as e:
        print(f"❌ Erro na requisição à API: {e}")
        return []
    except json.JSONDecodeError:
        print("❌ Erro: A resposta da IA não era um JSON válido.")
        # Opcional: pode guardar 'texto_gerado' num ficheiro para depuração
        return []
    except (IndexError, KeyError) as e:
        print(
            f"❌ Erro: A resposta da API não continha o formato esperado. Detalhe: {e}")
        return []
