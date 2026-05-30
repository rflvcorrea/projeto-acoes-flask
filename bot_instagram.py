import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

USUARIO = os.getenv("INSTAGRAM_USER")
SENHA = os.getenv("INSTAGRAM_PASS")


def abrir_instagram():
    opcoes = Options()
    opcoes.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opcoes,
    )
    return driver


def fazer_login(driver):
    driver.get("https://www.instagram.com")

    wait = WebDriverWait(driver, 15)

    campo_usuario = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    campo_usuario.send_keys(USUARIO)

    campo_senha = driver.find_element(By.NAME, "password")
    campo_senha.send_keys(SENHA)

    botao_login = driver.find_element(By.XPATH, "//button[@type='submit']")
    botao_login.click()

    print("Login enviado, aguardando...")
    time.sleep(5)
    print("Login concluído.")


if __name__ == "__main__":
    if not USUARIO or not SENHA:
        print("Erro: preencha INSTAGRAM_USER e INSTAGRAM_PASS no arquivo .env")
    else:
        driver = abrir_instagram()
        fazer_login(driver)
        input("Pressione Enter para fechar o navegador...")
        driver.quit()
