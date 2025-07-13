# generator_Bank.py

import csv
import json
import random
from faker import Faker
from pathlib import Path

# --- Constantes ---
fake = Faker('pt_BR')
BANCOS = ["Banco do Brasil", "Caixa Econômica Federal",
          "Santander", "Bradesco", "Itaú", "Nubank", "Inter"]
TIPOS_CONTA = ["Corrente", "Poupança"]


def gerar_cpf_valido() -> str:
    """Gera um número de CPF válido com os dígitos verificadores corretos."""
    cpf_base = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        soma = sum(n * (len(cpf_base) + 1 - i) for i, n in enumerate(cpf_base))
        digito = 11 - (soma % 11)
        cpf_base.append(digito if digito < 10 else 0)
    return "".join(map(str, cpf_base))


def gerar_massa_bancaria(quantidade: int = 5, permitir_saldo_negativo: bool = False) -> list[dict]:
    """Gera uma lista de dados bancários fictícios."""
    dados_bancarios = []
    for _ in range(quantidade):
        saldo = round(random.uniform(-5000, 100000)
                      if permitir_saldo_negativo else random.uniform(0, 100000), 2)
        dados_bancarios.append({
            "Banco": random.choice(BANCOS),
            "Agência": f"{fake.random_int(min=100, max=9999):04}",
            "Conta": f"{fake.random_int(min=10000, max=99999)}-{fake.random_int(min=0, max=9)}",
            "Tipo de Conta": random.choice(TIPOS_CONTA),
            "Titular": fake.name(),
            "CPF": gerar_cpf_valido(),
            "E-mail": fake.email(),
            "Telefone": fake.phone_number(),
            "Saldo": saldo,
            "Data de Abertura": fake.date_between(start_date='-10y', end_date='today').strftime('%d/%m/%Y'),
        })
    return dados_bancarios


def salvar_massa_bancaria_csv(dados: list[dict], caminho_arquivo: Path):
    """Salva os dados bancários em um ficheiro CSV."""
    with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)
    print(f"✅ Arquivo '{caminho_arquivo}' gerado com sucesso!")

# Adicione outras funções (salvar_json, buscar_contas, etc.) se necessário,
# seguindo o mesmo padrão de receber os dados como argumento.
