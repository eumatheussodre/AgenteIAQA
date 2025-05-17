import csv
from faker import Faker
import random

fake = Faker()

def gerar_massa_bancaria(quantidade=5):
    bancos = ["Banco do Brasil", "Caixa Econômica Federal", "Santander", "Bradesco", "Itaú", "Nubank", "Inter"]
    tipos_conta = ["Corrente", "Poupança"]

    dados_bancarios = []
    for _ in range(quantidade):
        banco = random.choice(bancos)
        agencia = fake.random_int(min=1000, max=9999)
        conta = f"{fake.random_int(min=100000, max=999999)}-{fake.random_int(min=0, max=9)}"
        tipo_conta = random.choice(tipos_conta)
        
        dados_bancarios.append({
            "Banco": banco,
            "Agência": agencia,
            "Conta": conta,
            "Tipo de Conta": tipo_conta,
            "Titular": fake.name(),
            "CPF": fake.random_int(min=10000000000, max=99999999999)
        })
    
    return dados_bancarios

def salvar_massa_bancaria_csv(nome_arquivo="massa_bancaria.csv", quantidade=5):
    dados_bancarios = gerar_massa_bancaria(quantidade)

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=dados_bancarios[0].keys())
        writer.writeheader()
        writer.writerows(dados_bancarios)

    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")
