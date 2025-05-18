from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

def criar_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)

def executar_teste_simples():
    driver = criar_driver()
    resultado = {"status": "success", "mensagem": "", "screenshot": None}
    try:
        driver.get("https://example.com")
        titulo = driver.title
        assert "Example" in titulo
        resultado["mensagem"] = "✅ Teste executado com sucesso."
    except Exception as e:
        screenshot_path = salvar_screenshot(driver, "falha_teste_simples.png")
        resultado["status"] = "fail"
        resultado["mensagem"] = f"❌ Falha no teste: {e}"
        resultado["screenshot"] = screenshot_path
    finally:
        driver.quit()
    return resultado

def executar_teste_login(url, usuario, senha, campo_usuario_id, campo_senha_id, botao_login_id, texto_sucesso):
    driver = criar_driver()
    resultado = {"status": "success", "mensagem": "", "screenshot": None}
    try:
        driver.get(url)
        time.sleep(1)
        driver.find_element(By.ID, campo_usuario_id).send_keys(usuario)
        driver.find_element(By.ID, campo_senha_id).send_keys(senha)
        driver.find_element(By.ID, botao_login_id).click()
        time.sleep(2)
        assert texto_sucesso in driver.page_source
        resultado["mensagem"] = "✅ Login realizado com sucesso."
    except Exception as e:
        screenshot_path = salvar_screenshot(driver, "falha_login.png")
        resultado["status"] = "fail"
        resultado["mensagem"] = f"❌ Falha no login: {e}"
        resultado["screenshot"] = screenshot_path
    finally:
        driver.quit()
    return resultado

def salvar_screenshot(driver, filename):
    pasta = "screenshots"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, filename)
    driver.save_screenshot(caminho)
    return caminho
