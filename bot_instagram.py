from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def abrir_instagram():
    opcoes = Options()
    opcoes.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opcoes,
    )

    driver.get("https://www.instagram.com")
    print("Instagram aberto com sucesso.")
    time.sleep(5)

    return driver


if __name__ == "__main__":
    driver = abrir_instagram()
    input("Pressione Enter para fechar o navegador...")
    driver.quit()
