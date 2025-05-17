from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def executar_teste_simples():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://example.com")
        titulo = driver.title
        assert "Example" in titulo
        return "✅ Teste executado com sucesso."
    except Exception as e:
        return f"❌ Falha no teste: {e}"
    finally:
        driver.quit()
