from faker import Faker  # Importação correta
fake = Faker()

def gerar_massa_de_dados(quantidade=5):
    registros = []
    for _ in range(quantidade):
        registro = {
            "nome": fake.name(),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "endereco": fake.address(),
            "data_de_nascimento": fake.date_of_birth(),
        }
        registros.append(registro)
    return registros
