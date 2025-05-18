import requests
import json
import re

def validar_url(url):
    return re.match(r'^https?://', url) is not None

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

def enviar_requisicao(url, metodo, payload=None, headers=None):
    """Executa requisições HTTP e retorna resposta formatada."""
    print(f"\n🚀 Executando {metodo} em {url}...")
    try:
        if metodo == "GET":
            resposta = requests.get(url, headers=headers, timeout=5)
        elif metodo == "POST":
            resposta = requests.post(url, json=payload, headers=headers, timeout=5)
        elif metodo == "PUT":
            resposta = requests.put(url, json=payload, headers=headers, timeout=5)
        elif metodo == "DELETE":
            resposta = requests.delete(url, headers=headers, timeout=5)
        else:
            print("❌ Método HTTP inválido!")
            return

        print(f"📡 Status HTTP: {resposta.status_code}")
        print(f"⏳ Tempo de resposta: {resposta.elapsed.total_seconds()} segundos")
        print(f"📦 Headers da resposta: {dict(resposta.headers)}")
        try:
            resposta_json = resposta.json()
            print(f"📥 Resposta da API:\n{json.dumps(resposta_json, indent=4, ensure_ascii=False)}")
        except Exception:
            print(f"📥 Resposta da API (texto):\n{resposta.text}")

        # Salvar resposta em arquivo
        salvar = input("💾 Deseja salvar a resposta em um arquivo? (s/n) ➜ ").strip().lower()
        if salvar == "s":
            nome_arquivo = input("📝 Nome do arquivo (ex: resposta.json): ").strip() or "resposta.json"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                try:
                    json.dump(resposta_json, f, ensure_ascii=False, indent=4)
                except Exception:
                    f.write(resposta.text)
            print(f"✅ Resposta salva em '{nome_arquivo}'.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao executar requisição: {e}")

def ler_headers():
    headers = {}
    while True:
        chave = input("🔑 Header (ou pressione Enter para continuar): ").strip()
        if not chave:
            break
        valor = input(f"Valor para '{chave}': ").strip()
        headers[chave] = valor
    return headers if headers else None

if __name__ == "__main__":
    print("\n=== 🛠️ Testador de API - Tipo Postman ===")
    while True:
        url_api = input("🔗 Insira a URL da API ➜ ").strip()
        if not validar_url(url_api):
            print("❌ URL inválida! Deve começar com http:// ou https://")
            continue

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
                    payload_str = input("📤 Insira o payload JSON para envio (ou deixe em branco) ➜ ").strip()
                    if payload_str:
                        try:
                            payload = json.loads(payload_str)
                        except Exception as e:
                            print(f"❌ Payload JSON inválido: {e}")
                            continue

                print("\nDeseja adicionar headers personalizados?")
                add_headers = input("Digite 's' para sim ou Enter para não ➜ ").strip().lower()
                headers = ler_headers() if add_headers == "s" else None

                enviar_requisicao(url_api, metodos[escolha], payload, headers)
            else:
                print("❌ Opção inválida!")
        else:
            print("❌ API não está acessível! Verifique a URL e tente novamente.")

        repetir = input("\n🔁 Deseja testar outra requisição? (s/n) ➜ ").strip().lower()
        if repetir != "s":
            print("👋 Encerrando o testador de API.")
            break
