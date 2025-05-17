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
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
        return []

    resultado = response.json()
    print("DEBUG - resposta bruta da API:", resultado)  # ✅ Log extra para depuração

    if not resultado or 'generated_text' not in resultado[0]:
        print("⚠️ Erro: IA não gerou resposta válida!")
        return []

    texto_gerado = resultado[0]['generated_text']
    print("\nDEBUG - texto gerado pela IA:", texto_gerado)  # ✅ Log extra para depuração

    # Melhor separação dos casos de teste
    partes = re.split(r"(ID:\s*CT-\d+)", texto_gerado)
    casos = []
    for i in range(1, len(partes), 2):
        id_ct = partes[i].strip()
        conteudo = partes[i + 1].strip() if i + 1 < len(partes) else ""

        res_esperado_match = re.search(r"(Resultado Esperado:.*)", conteudo, flags=re.IGNORECASE)
        resultado_esperado = res_esperado_match.group(1).strip() if res_esperado_match else "Resultado Esperado: [Definir corretamente]"

        conteudo = re.sub(r"Resultado Esperado:.*", "", conteudo, flags=re.IGNORECASE).strip()
        etapas = [linha.strip("- ").strip() for linha in conteudo.splitlines() if linha.strip()]

        caso_formatado = f"{id_ct}\nDescrição: {conteudo.splitlines()[0]}\n"  # Usa a primeira linha do conteúdo como descrição
        
        # Remove a linha já usada como descrição antes de processar as etapas
        conteudo = "\n".join(conteudo.splitlines()[1:]).strip()

        # Processa as etapas corretamente
        etapas = [linha.strip("- ").strip() for linha in conteudo.splitlines() if linha.strip()]
        
        for etapa in etapas:
            caso_formatado += f"- {etapa}\n"

        caso_formatado += f"\n{resultado_esperado}\n"
        casos.append(caso_formatado)


    if not casos:
        print("⚠️ Nenhum caso de teste foi extraído corretamente!")
    
    return casos  # ✅ Agora garantimos que os casos estão sendo retornados corretamente
