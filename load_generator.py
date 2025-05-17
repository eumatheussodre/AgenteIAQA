from file_generator import salvar_json, salvar_csv

def gerar_e_salvar_testes():
    """Gera os testes de carga e salva os arquivos."""
    json_path = "/app/downloads/massa_carga.json"
    csv_path = "/app/downloads/massa_carga.csv"
    
    salvar_json(json_path, 10000)
    salvar_csv(csv_path, 10000)

gerar_e_salvar_testes()
