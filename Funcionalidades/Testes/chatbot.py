def responder_pergunta(pergunta):
    pergunta = pergunta.lower()
    if "teste" in pergunta and "automatizado" in pergunta:
        return "Testes automatizados são executados por scripts para validar funcionalidades sem intervenção humana."
    elif "azure" in pergunta:
        return "Você pode enviar casos de teste diretamente para Azure DevOps usando seu token de acesso."
    else:
        return "Desculpe, não entendi. Tente reformular sua pergunta."
