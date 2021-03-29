from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import threading
import json
import time

lock = threading.Lock()

pokemons = []
scores = []

def autotest(begin, end):

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)

    driver.get("https://pvpoketw.com/team-builder/")

    time.sleep(1.5)

    setting = driver.find_element_by_class_name("arrow-down")
    setting.click()

    fill_team = Select(driver.find_element_by_class_name("quick-fill-select"))
    fill_team.select_by_index(1)

    time.sleep(0.5)

    firstTime = True

    for pokeTeamsCount in range(begin//6, end//6):
        print(f"now processing team {pokeTeamsCount}")

        if firstTime:
            for pokeTeamIndex in range(1, 7):
                add_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[1]/div/div[1]/button[1]")))
                add_button.click()

                choose_pokemon = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/select")))
                pokemons = choose_pokemon.text.split('\n')

                fill_pokemon = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/input")))
                fill_pokemon.send_keys(pokemons[pokeTeamsCount*6 + pokeTeamIndex].strip())

                add = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".save-poke")))
                add.click()

                firstTime = False
        else:
            for pokeTeamIndex in range(1, 7):
                try:
                    find_pokemon = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[{pokeTeamIndex}]/div[1]")))
                    find_pokemon.click()

                    choose_pokemon = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/select")))

                    fill_pokemon = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/input")))
                    fill_pokemon.send_keys(pokemons[pokeTeamsCount*6 + pokeTeamIndex].strip())

                    add = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".save-poke")))
                    add.click()
                except:
                    continue
                

        submit = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rate-btn")))
        submit.click()

        time.sleep(3)

        for pokeTeamIndex in range(1, 7):
            nameElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/h2")))
            scoreElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/div[4]/span")))

            with lock:
                scores.append({"name": nameElement.text,
                          "score": int(scoreElement.text)})


if __name__ == "__main__":
    time_start = time.time()

    threads = []

    for i in range(5):
        t = threading.Thread(target=autotest, args=(450*i, 450*(i+1),))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    result = sorted(scores, key=lambda k: k["score"], reverse=True)

    print(result)

    f = open("result.json", "w", encoding="utf-8")
    json.dump(result, f, ensure_ascii=False)
    f.close()

    time_end = time.time()

    print(f"time cost: {time_end - time_start} secs")
