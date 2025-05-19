import requests
import re

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_TOKEN = "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"  # Substitua pelo seu token correto

def gerar_casos_de_teste(texto_requisitos_dev, texto_requisitos_spec):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    prompt = (
        "Analise **ambos** os documentos abaixo e gere **casos de teste planejados** "
        "com base nas funcionalidades descritas.\n\n"
        "**Documento do Desenvolvedor:**\n"
        f"{texto_requisitos_dev}\n\n"
        "**Especificação Funcional:**\n"
        f"{texto_requisitos_spec}\n\n"
        "**Formato esperado:**\n"
        "ID: CT-XXX\n"
        "Descrição: [Descrição detalhada do teste]\n"
        "- Etapa 1\n"
        "- Etapa 2\n"
        "Resultado Esperado: [O resultado esperado]\n\n"
    )

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.5},
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        resultado = response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return []

    print("DEBUG - resposta bruta da API:", resultado)

    # Verifica se a resposta está no formato esperado
    texto_gerado = ""
    if isinstance(resultado, list) and resultado and 'generated_text' in resultado[0]:
        texto_gerado = resultado[0]['generated_text']
    elif isinstance(resultado, dict) and 'generated_text' in resultado:
        texto_gerado = resultado['generated_text']
    else:
        print("⚠️ Erro: IA não gerou resposta válida!")
        return []

    print("\nDEBUG - texto gerado pela IA:", texto_gerado)

    # Extrai casos de teste usando regex
    casos = []
    padrao = r"(ID:\s*CT-\d+)(.*?)(?=ID:\s*CT-\d+|$)"
    for match in re.finditer(padrao, texto_gerado, re.DOTALL):
        id_ct = match.group(1).strip()
        conteudo = match.group(2).strip()

        descricao_match = re.search(r"Descrição:(.*?)(?:-|\n|$)", conteudo, re.DOTALL)
        descricao = descricao_match.group(1).strip() if descricao_match else "[Descrição não encontrada]"

        etapas = re.findall(r"-\s*(.*)", conteudo)
        resultado_esperado_match = re.search(r"Resultado Esperado:(.*)", conteudo)
        resultado_esperado = resultado_esperado_match.group(1).strip() if resultado_esperado_match else "[Resultado não encontrado]"

        caso_formatado = f"{id_ct}\nDescrição: {descricao}\n"
        for etapa in etapas:
            caso_formatado += f"- {etapa}\n"
        caso_formatado += f"\nResultado Esperado: {resultado_esperado}\n"
        casos.append(caso_formatado)

    if not casos:
        print("⚠️ Nenhum caso de teste foi extraído corretamente!")

    return casos