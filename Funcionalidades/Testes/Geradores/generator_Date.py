from faker import Faker
import random
import csv
import json

fake = Faker('pt_BR')

CAMPOS_DISPONIVEIS = [
    "ID", "Nome", "Email", "Telefone", "Endereço", "Data de Nascimento",
    "Empresa", "Salário", "CPF", "CNPJ"
]

def gerar_massa_de_dados(quantidade, campos):
    fake = Faker('pt_BR')
    dados = []
    for _ in range(quantidade):
        registro = {}
        for campo in campos:
            if campo == "nome":
                registro["nome"] = fake.name()
            elif campo == "email":
                registro["email"] = fake.email()
            elif campo == "cpf":
                registro["cpf"] = fake.cpf()
            elif campo == "cnpj":
                registro["cnpj"] = fake.cnpj()
            elif campo == "telefone":
                registro["telefone"] = fake.phone_number()
            elif campo == "endereco":
                registro["endereco"] = fake.address().replace('\n', ', ')
            elif campo == "data_nascimento":
                registro["data_nascimento"] = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d/%m/%Y')
        dados.append(registro)
    return dados

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

if __name__ == "__main__":
    campos = ["nome", "email", "cpf", "telefone", "endereco", "data_nascimento"]
    dados = gerar_massa_de_dados(10, campos)
    salvar_dados_csv(dados)
    salvar_dados_json(dados)