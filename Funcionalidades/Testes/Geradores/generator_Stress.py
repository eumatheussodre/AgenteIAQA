import os
import csv
import json
import random
import multiprocessing
from faker import Faker

fake = Faker()
DOWNLOADS_PATH = "downloads"
os.makedirs(DOWNLOADS_PATH, exist_ok=True)

CAMPOS_DISPONIVEIS = {
    "ID": lambda: fake.uuid4(),
    "Nome": lambda: fake.name(),
    "Email": lambda: fake.email(),
    "Endereço": lambda: fake.address().replace('\n', ', '),
    "Telefone": lambda: fake.phone_number(),
    "Data de Nascimento": lambda: fake.date_of_birth().strftime("%Y-%m-%d"),
    "Empresa": lambda: fake.company(),
    "Salário": lambda: round(random.uniform(2000, 15000), 2)
}

def gerar_massa_carga(quantidade: int, campos: list[str]) -> list[dict]:
    """Gera uma lista de dicionários com dados fake para testes de carga."""
    return [
        {campo: CAMPOS_DISPONIVEIS[campo]() for campo in campos}
        for _ in range(quantidade)
    ]

def salvar_arquivo(nome_arquivo: str, dados: list[dict], tipo: str):
    """Salva os dados gerados em um arquivo CSV ou JSON."""
    print(f"⏳ Salvando arquivo: {nome_arquivo}...")
    with open(nome_arquivo, mode='w', encoding='utf-8', newline='' if tipo == "csv" else None) as arquivo:
        if tipo == "csv":
            writer = csv.DictWriter(arquivo, fieldnames=dados[0].keys())
            writer.writeheader()
            writer.writerows(dados)
        else:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo salvo em: {nome_arquivo}")

def gerar_e_salvar(quantidade: int, campos: list[str], formatos: list[str]):
    """Executa a geração e salvamento dos arquivos em paralelo."""
    print(f"🔥 Gerando {quantidade} registros de massa de dados com campos: {', '.join(campos)}...")

    # Divide a carga entre múltiplos processos
    num_processos = min(multiprocessing.cpu_count(), quantidade)  
    carga_por_processo = quantidade // num_processos
    resto = quantidade % num_processos
    cargas = [carga_por_processo + (1 if i < resto else 0) for i in range(num_processos)]
    pool = multiprocessing.Pool(num_processos)
    
    resultados = pool.starmap(gerar_massa_carga, [(c, campos) for c in cargas])
    pool.close()
    pool.join()

    # Unifica os resultados
    dados = [registro for resultado in resultados for registro in resultado]

    # Salva os arquivos conforme o formato escolhido
    if "csv" in formatos:
        salvar_arquivo(f"{DOWNLOADS_PATH}/massa_carga.csv", dados, "csv")
    if "json" in formatos:
        salvar_arquivo(f"{DOWNLOADS_PATH}/massa_carga.json", dados, "json")

if __name__ == "__main__":
    print("\n=== ⚡ Gerador de Massa de Dados - Testes de Stress ===")
    try:
        registros = int(input("Quantos registros deseja gerar? (Ex: 1000000) ➜ ").strip())
    except Exception:
        print("Valor inválido. Saindo.")
        exit(1)

    print("\nCampos disponíveis:")
    for i, campo in enumerate(CAMPOS_DISPONIVEIS.keys(), 1):
        print(f"{i}. {campo}")
    campos_escolhidos = input("Digite os números dos campos desejados separados por vírgula (Ex: 1,2,3): ").strip()
    indices = [int(i) - 1 for i in campos_escolhidos.split(",") if i.strip().isdigit()]
    campos = [list(CAMPOS_DISPONIVEIS.keys())[i] for i in indices if 0 <= i < len(CAMPOS_DISPONIVEIS)]

    if not campos:
        print("Nenhum campo selecionado. Saindo.")
        exit(1)

    print("\nFormatos disponíveis para exportação:")
    print("1. CSV\n2. JSON\n3. Ambos")
    formato = input("Escolha o formato (1/2/3): ").strip()
    if formato == "1":
        formatos = ["csv"]
    elif formato == "2":
        formatos = ["json"]
    elif formato == "3":
        formatos = ["csv", "json"]
    else:
        print("Formato inválido. Saindo.")
        exit(1)

    gerar_e_salvar(registros, campos, formatos)

    print("\n📥 Arquivos prontos para download:")
    if "csv" in formatos:
        print(f"- CSV: {DOWNLOADS_PATH}/massa_carga.csv")
    if "json" in formatos:
        print(f"- JSON: {DOWNLOADS_PATH}/massa_carga.json")