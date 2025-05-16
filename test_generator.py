import openai

openai.api_key = "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"

def gerar_casos_de_teste(texto_requisitos):
    print("🧠 Gerando casos de teste com IA...")

    messages = [
        {"role": "system", "content": "Você é um assistente especializado em gerar casos de teste para software."},
        {"role": "user", "content": f"Com base no seguinte requisito, gere casos de teste numerados:\n\n{texto_requisitos}"}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # ou outro modelo que preferir
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )

    texto_resultado = response.choices[0].message.content.strip()
    casos = texto_resultado.split("\n")
    return casos

# Exemplo de uso
if __name__ == "__main__":
    requisito = "O sistema deve permitir que o usuário faça login usando email e senha."
    casos = gerar_casos_de_teste(requisito)
    for caso in casos:
        print(caso)
