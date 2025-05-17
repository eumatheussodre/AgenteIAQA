import os
import csv
import json
import random
import multiprocessing
from faker import Faker

fake = Faker()
DOWNLOADS_PATH = "downloads"
os.makedirs(DOWNLOADS_PATH, exist_ok=True)

def gerar_massa_carga(quantidade: int) -> list[dict]:
    """Gera uma lista de dicionários com dados fake para testes de carga."""
    return [{
        "ID": fake.uuid4(),
        "Nome": fake.name(),
        "Email": fake.email(),
        "Endereço": fake.address(),
        "Telefone": fake.phone_number(),
        "Data de Nascimento": fake.date_of_birth().strftime("%Y-%m-%d"),
        "Empresa": fake.company(),
        "Salário": round(random.uniform(2000, 15000), 2)
    } for _ in range(quantidade)]

def salvar_arquivo(nome_arquivo: str, dados: list[dict], tipo: str):
    """Salva os dados gerados em um arquivo CSV ou JSON."""
    print(f"⏳ Salvando arquivo: {nome_arquivo}...")
    with open(nome_arquivo, mode='w', encoding='utf-8') as arquivo:
        if tipo == "csv":
            writer = csv.DictWriter(arquivo, fieldnames=dados[0].keys())
            writer.writeheader()
            writer.writerows(dados)
        else:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo salvo em: {nome_arquivo}")

def gerar_e_salvar(quantidade: int):
    """Executa a geração e salvamento dos arquivos em paralelo."""
    print(f"🔥 Gerando {quantidade} registros de massa de dados...")

    # Divide a carga entre múltiplos processos
    num_processos = multiprocessing.cpu_count()  
    carga_por_processo = quantidade // num_processos
    pool = multiprocessing.Pool(num_processos)
    
    resultados = pool.map(gerar_massa_carga, [carga_por_processo] * num_processos)
    pool.close()
    pool.join()

    # Unifica os resultados
    dados = [registro for resultado in resultados for registro in resultado]

    # Salva os arquivos
    salvar_arquivo(f"{DOWNLOADS_PATH}/massa_carga.csv", dados, "csv")
    salvar_arquivo(f"{DOWNLOADS_PATH}/massa_carga.json", dados, "json")

if __name__ == "__main__":
    print("\n=== ⚡ Gerador de Massa de Dados - Testes de Stress ===")
    registros = int(input("Quantos registros deseja gerar? (Ex: 1000000) ➜ ").strip())
    
    gerar_e_salvar(registros)
    
    print("📥 Arquivos prontos para download:")
    print(f"- CSV: {DOWNLOADS_PATH}/massa_carga.csv")
    print(f"- JSON: {DOWNLOADS_PATH}/massa_carga.json")
