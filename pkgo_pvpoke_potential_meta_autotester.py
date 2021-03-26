from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

def autotest():
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)

    driver.get("https://pvpoketw.com/team-builder/")

    time.sleep(1)

    setting = driver.find_element_by_class_name("arrow-down")
    setting.click()

    fill_team = Select(driver.find_element_by_class_name("quick-fill-select"))
    fill_team.select_by_index(1)

    add_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[1]/div/div[1]/button[1]")))
    add_button.click()

    # /html/body/div/div/div[3]/div[1]/div/div[1]/button[1]

    time.sleep(100)

if __name__ == "__main__":
    autotest()