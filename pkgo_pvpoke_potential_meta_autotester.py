from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time


def autotest():
    scores = []

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)

    driver.get("https://pvpoketw.com/team-builder/")

    time.sleep(1)

    setting = driver.find_element_by_class_name("arrow-down")
    setting.click()

    fill_team = Select(driver.find_element_by_class_name("quick-fill-select"))
    fill_team.select_by_index(1)

    time.sleep(1)

    for pokeTeamsCount in range(2000//6):
        for pokeTeamIndex in range(1, 7):
            add_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[1]/div/div[1]/button[1]")))
            add_button.click()

            choose_pokemon = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/select")))
            for selectTimes in range(pokeTeamsCount*6 + pokeTeamIndex):
                choose_pokemon.send_keys(Keys.RIGHT)

            add = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".save-poke")))
            add.click()

        submit = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rate-btn")))
        submit.click()

        time.sleep(3)

        for pokeTeamIndex in range(1, 7):
            nameElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/h2")))
            scoreElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/div[4]/span")))

            scores.append({"name": nameElement.text,
                          "score": int(scoreElement.text)})

        time.sleep(2)

        clear = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/a")))
        clear.click()

        clear_confirm = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div/div/div[1]")))
        clear_confirm.click()

    print(scores)

    time.sleep(100)


if __name__ == "__main__":
    autotest()
