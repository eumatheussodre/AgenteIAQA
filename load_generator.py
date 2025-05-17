import csv
import json
from faker import Faker
import random
from concurrent.futures import ThreadPoolExecutor

fake = Faker()

def gerar_massa_carga(quantidade=10000):
    dados = []
    for _ in range(quantidade):
        dados.append({
            "ID": fake.uuid4(),
            "Nome": fake.name(),
            "Email": fake.email(),
            "Endereço": fake.address(),
            "Telefone": fake.phone_number(),
            "Data de Nascimento": fake.date_of_birth(),
            "Empresa": fake.company(),
            "Salário": round(random.uniform(2000, 15000), 2)
        })
    return dados

def salvar_csv(nome_arquivo="massa_carga.csv", quantidade=10000):
    dados = gerar_massa_carga(quantidade)
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)
    print(f"✅ Arquivo CSV '{nome_arquivo}' gerado!")

def salvar_json(nome_arquivo="massa_carga.json", quantidade=10000):
    
    dados = gerar_massa_carga(quantidade)
    with open(nome_arquivo, mode='w', encoding='utf-8') as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo JSON '{nome_arquivo}' gerado!")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(salvar_csv, "massa_carga.csv", 10000)
        executor.submit(salvar_json, "massa_carga.json", 10000)
