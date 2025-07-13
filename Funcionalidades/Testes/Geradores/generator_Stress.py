# generator_Stress.py

import csv
import json
import multiprocessing
import random
from faker import Faker
from pathlib import Path
from typing import List, Dict, Callable, Any

# --- Constantes e Configuração ---
fake = Faker('pt_BR')
# Cria o diretório de downloads de forma segura
DOWNLOADS_PATH = Path("downloads")
DOWNLOADS_PATH.mkdir(exist_ok=True)

# Dicionário de geradores para fácil extensão
CAMPOS_DISPONIVEIS: Dict[str, Callable[[], Any]] = {
    "ID": lambda: fake.uuid4(),
    "Nome": lambda: fake.name(),
    "Email": lambda: fake.email(),
    "Endereço": lambda: fake.address().replace('\n', ', '),
    "Telefone": lambda: fake.phone_number(),
    "Data de Nascimento": lambda: fake.date_of_birth().strftime("%Y-%m-%d"),
    "Empresa": lambda: fake.company(),
    "Salário": lambda: round(random.uniform(2000, 15000), 2)
}


def gerar_lote_de_massa(quantidade: int, campos: List[str]) -> List[Dict]:
    """Gera uma lista de dicionários com dados fake."""
    return [{campo: CAMPOS_DISPONIVEIS[campo]() for campo in campos} for _ in range(quantidade)]


def salvar_arquivo(caminho_arquivo: Path, dados: List[Dict], tipo: str):
    """Salva os dados gerados em um ficheiro CSV ou JSON."""
    print(f"⏳ Salvando arquivo: {caminho_arquivo}...")
    try:
        with caminho_arquivo.open(mode='w', encoding='utf-8', newline='' if tipo == "csv" else None) as f:
            if tipo == "csv":
                writer = csv.DictWriter(f, fieldnames=dados[0].keys())
                writer.writeheader()
                writer.writerows(dados)
            else:  # JSON
                json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"✅ Arquivo salvo com sucesso: {caminho_arquivo}")
    except IOError as e:
        print(f"❌ Erro ao salvar o ficheiro: {e}")


def gerar_e_salvar_em_paralelo(quantidade: int, campos: List[str], formatos: List[str]):
    """Orquestra a geração de dados em paralelo e o salvamento dos ficheiros."""
    print(
        f"🔥 Gerando {quantidade} registros com campos: {', '.join(campos)}...")

    # Limita a 4 processos para não sobrecarregar
    num_processos = min(multiprocessing.cpu_count(), 4)
    carga_por_processo = quantidade // num_processos
    cargas = [carga_por_processo] * num_processos
    for i in range(quantidade % num_processos):  # Distribui o resto
        cargas[i] += 1

    with multiprocessing.Pool(processes=num_processos) as pool:
        resultados_parciais = pool.starmap(
            gerar_lote_de_massa, [(c, campos) for c in cargas])

    dados_completos = [
        registro for resultado in resultados_parciais for registro in resultado]

    if "csv" in formatos:
        salvar_arquivo(DOWNLOADS_PATH / "massa_carga.csv",
                       dados_completos, "csv")
    if "json" in formatos:
        salvar_arquivo(DOWNLOADS_PATH / "massa_carga.json",
                       dados_completos, "json")

# A interface de linha de comando (bloco if __name__ == "__main__") pode ser mantida como está,
# pois já é funcional para testes do módulo.
