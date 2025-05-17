import requests
import json

def testar_conexao(url):
    """Testa se a API está acessível e retorna o status."""
    print(f"\n🔍 Testando conexão com {url}...")
    
    try:
        resposta = requests.get(url, timeout=5)
        print(f"✅ API acessível! Status HTTP: {resposta.status_code}")
        return resposta.status_code
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def enviar_requisicao(url, metodo, payload=None):
    """Executa requisições HTTP e retorna resposta formatada."""
    print(f"\n🚀 Executando {metodo} em {url}...")
    
    try:
        if metodo == "GET":
            resposta = requests.get(url, timeout=5)
        elif metodo == "POST":
            resposta = requests.post(url, json=payload, timeout=5)
        elif metodo == "PUT":
            resposta = requests.put(url, json=payload, timeout=5)
        elif metodo == "DELETE":
            resposta = requests.delete(url, timeout=5)
        else:
            print("❌ Método HTTP inválido!")
            return
        
        print(f"📡 Status HTTP: {resposta.status_code}")
        print(f"⏳ Tempo de resposta: {resposta.elapsed.total_seconds()} segundos")
        print(f"📥 Resposta da API:\n{json.dumps(resposta.json(), indent=4, ensure_ascii=False)}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao executar requisição: {e}")

if __name__ == "__main__":
    print("\n=== 🛠️ Testador de API - Tipo Postman ===")
    
    url_api = input("🔗 Insira a URL da API ➜ ").strip()
    if testar_conexao(url_api):
        print("\n🛠️ Escolha o método HTTP:")
        print("1️⃣ - GET")
        print("2️⃣ - POST")
        print("3️⃣ - PUT")
        print("4️⃣ - DELETE")
        
        escolha = input("\nDigite a opção desejada ➜ ").strip()
        metodos = {"1": "GET", "2": "POST", "3": "PUT", "4": "DELETE"}
        
        if escolha in metodos:
            payload = None
            if escolha in ["2", "3"]:  # POST ou PUT requer payload
                payload = input("📤 Insira o payload JSON para envio (ou deixe em branco) ➜ ").strip()
                payload = json.loads(payload) if payload else None

            enviar_requisicao(url_api, metodos[escolha], payload)
        else:
            print("❌ Opção inválida!")
    else:
        print("❌ API não está acessível! Verifique a URL e tente novamente.")
