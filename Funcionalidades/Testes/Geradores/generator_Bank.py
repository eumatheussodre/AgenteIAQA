import csv
import json
from faker import Faker
import random
from datetime import datetime

fake = Faker()

def gerar_cpf_valido():
    # Gera um CPF válido (simples, não garante validade real)
    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        val = sum([(len(cpf)+1-i)*v for i, v in enumerate(cpf)]) % 11
        cpf.append(0 if val < 2 else 11 - val)
    return ''.join(map(str, cpf))

def gerar_massa_bancaria(quantidade=5, saldo_negativo=False):
    bancos = ["Banco do Brasil", "Caixa Econômica Federal", "Santander", "Bradesco", "Itaú", "Nubank", "Inter"]
    tipos_conta = ["Corrente", "Poupança"]

    dados_bancarios = []
    for _ in range(quantidade):
        banco = random.choice(bancos)
        agencia = fake.random_int(min=1000, max=9999)
        conta = f"{fake.random_int(min=100000, max=999999)}-{fake.random_int(min=0, max=9)}"
        tipo_conta = random.choice(tipos_conta)
        saldo = round(random.uniform(-5000, 100000), 2) if saldo_negativo else round(random.uniform(0, 100000), 2)
        dados_bancarios.append({
            "Banco": banco,
            "Agência": agencia,
            "Conta": conta,
            "Tipo de Conta": tipo_conta,
            "Titular": fake.name(),
            "CPF": gerar_cpf_valido(),
            "E-mail": fake.email(),
            "Telefone": fake.phone_number(),
            "Saldo Inicial": saldo,
            "Data de Abertura": fake.date_between(start_date='-10y', end_date='today').strftime('%d/%m/%Y')
        })
    return dados_bancarios

def salvar_massa_bancaria_csv(nome_arquivo="massa_bancaria.csv", quantidade=5, saldo_negativo=False):
    dados_bancarios = gerar_massa_bancaria(quantidade, saldo_negativo)
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=dados_bancarios[0].keys())
        writer.writeheader()
        writer.writerows(dados_bancarios)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")

def salvar_massa_bancaria_json(nome_arquivo="massa_bancaria.json", quantidade=5, saldo_negativo=False):
    dados_bancarios = gerar_massa_bancaria(quantidade, saldo_negativo)
    with open(nome_arquivo, mode='w', encoding='utf-8') as arquivo_json:
        json.dump(dados_bancarios, arquivo_json, ensure_ascii=False, indent=4)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")

def buscar_contas_por_banco(dados, banco_nome):
    return [conta for conta in dados if conta["Banco"].lower() == banco_nome.lower()]

def buscar_contas_por_titular(dados, nome_titular):
    return [conta for conta in dados if nome_titular.lower() in conta["Titular"].lower()]

def validar_cpf(cpf):
    # Validação simples de CPF (apenas tamanho e dígitos)
    return isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit()

# Exemplo de uso para QA:
if __name__ == "__main__":
    # Gera 10 contas, algumas com saldo negativo
    salvar_massa_bancaria_csv("massa_bancaria.csv", quantidade=10, saldo_negativo=True)
    salvar_massa_bancaria_json("massa_bancaria.json", quantidade=10, saldo_negativo=True)

    # Busca contas do Itaú
    massa = gerar_massa_bancaria(10)
    contas_itau = buscar_contas_por_banco(massa, "Itaú")
    print(f"Contas do Itaú: {contas_itau}")

    # Busca contas por titular
    if massa:
        nome = massa[0]["Titular"].split()[0]
        contas_titular = buscar_contas_por_titular(massa, nome)
        print(f"Contas do titular '{nome}': {contas_titular}")

    # Validação de CPF
    print("CPF válido?", validar_cpf(massa[0]["CPF"]))
