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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://pvpoketw.com/team-builder/")

    # time.sleep(2.5)

    # setting = driver.find_element_by_class_name("arrow-down")
    # setting.click()

    # fill_team = Select(driver.find_element_by_class_name("quick-fill-select"))
    # fill_team.select_by_index(1)

    time.sleep(2.5)

    firstTime = True

    for pokeTeamsCount in range(begin//6, end//6):
        print(f"now processing team {pokeTeamsCount}")

        if firstTime:
            for pokeTeamIndex in range(1, 7):
                add_button = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div/div[1]/button[1]")))
                add_button.click()

                global pokemons
                if not pokemons:
                    choose_pokemon = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/select")))
                    pokemons = choose_pokemon.text.split('\n')

                    print("len of pokemons:", len(pokemons))

                fill_pokemon = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/input")))
                fill_pokemon.send_keys(
                    pokemons[pokeTeamsCount*6 + pokeTeamIndex].strip())

                add = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-poke")))
                add.click()

                firstTime = False
        else:
            for pokeTeamIndex in range(1, 7):
                try:
                    find_pokemon = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, f"/html/body/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[{pokeTeamIndex}]/div[1]")))
                    find_pokemon.click()

                    choose_pokemon = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/select")))

                    fill_pokemon = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div[1]/input")))
                    fill_pokemon.send_keys(
                        pokemons[pokeTeamsCount*6 + pokeTeamIndex].strip())

                    add = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-poke")))
                    add.click()
                except:
                    continue

        submit = None

        while submit is None:
            try:
                submit = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".rate-btn")))
                submit.click()
            except:
                pass

        time.sleep(0.1)

        for pokeTeamIndex in range(1, 7):
            name = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/h2"))).text
            score = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div[5]/div[5]/div/div[{pokeTeamIndex}]/div/div[4]/span"))).text

            with lock:
                scores.append({"name": name,
                               "score": int(score)})

    driver.quit()


if __name__ == "__main__":
    time_start = time.time()

    threads = []

    for i in range(10):
        t = threading.Thread(target=autotest, args=(210*i, 210*(i+1),))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    scores = [dict(tuple_item) for tuple_item in {
        tuple(dictionary.items()) for dictionary in scores}]
    result = sorted(scores, key=lambda k: k["score"], reverse=True)

    print(result)

    f = open("result.json", "w", encoding="utf-8")
    json.dump(result, f, ensure_ascii=False)
    f.close()

    time_end = time.time()

    print(f"time cost: {time_end - time_start} secs")
