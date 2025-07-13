# generator_Date.py

from faker import Faker
import csv
import json

# Instância única do Faker para o idioma português
fake = Faker('pt_BR')


def _get_geradores():
    """Retorna um dicionário que mapeia nomes de campos para funções geradoras."""
    return {
        "nome": fake.name,
        "email": fake.email,
        "cpf": fake.cpf,
        "cnpj": fake.cnpj,
        "telefone": fake.phone_number,
        "endereco": lambda: fake.address().replace('\n', ', '),
        "data_nascimento": lambda: fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d/%m/%Y'),
        "empresa": fake.company,
    }


def gerar_massa_de_dados(quantidade: int, campos: list[str]) -> list[dict]:
    """
    Gera uma massa de dados fictícios com base nos campos solicitados.

    Args:
        quantidade: O número de registros a serem gerados.
        campos: Uma lista de strings com os nomes dos campos desejados.

    Returns:
        Uma lista de dicionários, onde cada dicionário é um registro.
    """
    geradores = _get_geradores()
    dados = []

    for _ in range(quantidade):
        registro = {}
        for campo in campos:
            # Procura a função geradora no dicionário e a executa
            if campo in geradores:
                registro[campo] = geradores[campo]()
        if registro:
            dados.append(registro)

    return dados


def salvar_dados_csv(registros: list[dict], nome_arquivo: str = "massa_dados.csv"):
    """Salva uma lista de registros em um ficheiro CSV."""
    if not registros:
        print("⚠️ Nenhum registro para salvar.")
        return

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")


def salvar_dados_json(registros: list[dict], nome_arquivo: str = "massa_dados.json"):
    """Salva uma lista de registros em um ficheiro JSON."""
    if not registros:
        print("⚠️ Nenhum registro para salvar.")
        return

    with open(nome_arquivo, mode='w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)
    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")


# Bloco de execução para teste do módulo
if __name__ == "__main__":
    campos_desejados = ["nome", "email", "cpf", "telefone"]
    dados_gerados = gerar_massa_de_dados(10, campos_desejados)

    if dados_gerados:
        print("--- Dados Gerados ---")
        # Imprime os 2 primeiros
        print(json.dumps(dados_gerados[:2], indent=2, ensure_ascii=False))

        print("\n--- Salvando Arquivos ---")
        salvar_dados_csv(dados_gerados)
        salvar_dados_json(dados_gerados)
