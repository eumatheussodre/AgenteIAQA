from faker import Faker
import random
import csv
import json

fake = Faker('pt_BR')

CAMPOS_DISPONIVEIS = [
    "nome", "email", "telefone", "endereco", "data_de_nascimento",
    "cpf", "cnpj", "profissao", "data_cadastro", "status", "genero"
]

def gerar_massa_de_dados(
    quantidade=5,
    status_opcoes=None,
    generos_opcoes=None,
    campos=None
):
    if status_opcoes is None:
        status_opcoes = ["ativo", "inativo", "pendente", "bloqueado"]
    if generos_opcoes is None:
        generos_opcoes = ["Masculino", "Feminino", "Outro"]
    if campos is None:
        campos = CAMPOS_DISPONIVEIS

    registros = []
    for _ in range(quantidade):
        status = random.choice(status_opcoes)
        genero = random.choice(generos_opcoes)
        registro = {}
        if "nome" in campos:
            registro["nome"] = fake.name()
        if "email" in campos:
            registro["email"] = fake.email()
        if "telefone" in campos:
            registro["telefone"] = fake.phone_number()
        if "endereco" in campos:
            registro["endereco"] = fake.address().replace('\n', ', ')
        if "data_de_nascimento" in campos:
            registro["data_de_nascimento"] = fake.date_of_birth().strftime('%d/%m/%Y')
        if "cpf" in campos:
            registro["cpf"] = fake.cpf()
        if "cnpj" in campos:
            registro["cnpj"] = fake.cnpj()
        if "profissao" in campos:
            registro["profissao"] = fake.job()
        if "data_cadastro" in campos:
            registro["data_cadastro"] = fake.date_this_decade().strftime('%d/%m/%Y')
        if "status" in campos:
            registro["status"] = status
        if "genero" in campos:
            registro["genero"] = genero
        registros.append(registro)
    return registros

def salvar_dados_csv(registros, nome_arquivo="massa_dados.csv"):
    if not registros:
        return
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")

def salvar_dados_json(registros, nome_arquivo="massa_dados.json"):
    if not registros:
        return
    with open(nome_arquivo, mode='w', encoding='utf-8') as arquivo_json:
        json.dump(registros, arquivo_json, ensure_ascii=False, indent=4)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")

def filtrar_por_status(registros, status):
    return [r for r in registros if r.get("status", "").lower() == status.lower()]

def filtrar_por_nome(registros, nome):
    return [r for r in registros if nome.lower() in r.get("nome", "").lower()]

# Exemplo de uso para QA:
if __name__ == "__main__":
    # Exemplo: gerar apenas nome, email e cpf, apenas status "ativo" ou "pendente", e apenas gênero "Feminino"
    campos_escolhidos = ["nome", "email", "cpf"]
    status_escolhidos = ["ativo", "pendente"]
    generos_escolhidos = ["Feminino"]
    massa = gerar_massa_de_dados(
        quantidade=10,
        status_opcoes=status_escolhidos,
        generos_opcoes=generos_escolhidos,
        campos=campos_escolhidos
    )
    salvar_dados_csv(massa)
    salvar_dados_json(massa)
    ativos = filtrar_por_status(massa, "ativo")
    print(f"Registros ativos: {ativos}")
    if massa:
        nome = massa[0].get("nome", "").split()[0]
        print(f"Busca por nome '{nome}':", filtrar_por_nome(massa, nome))
