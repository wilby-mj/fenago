from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pickle
import re


def start_browser(url):
    options = Options()
    options.headless = True
    options.add_argument('window-size=1920x1080') 

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    #time.sleep(5)
    return driver

def accept_cookies(driver):
    try:
        accept = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        accept.click()
        time.sleep(5)
    except:
        pass

def choose_value_from_dropdown(driver):
    try:
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[contains(@data-test-id,"BTTS_FT")]')))
        dropdown.click()
        #time.sleep(5)
        #chooser = WebDriverWait(dropdown, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),'+'"'+str(market)+'"'+')]')))
        #chooser.click()
        #time.sleep(5)
    except:
        pass

def scrape_odds(driver):
    list_odds, teams = [], []
    #time.sleep(10)
    box = driver.find_element_by_xpath('//div[contains(@class,"tabs-content")]')
    rows = WebDriverWait(box, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'events-container.prematch')))
    for row in rows:
        odds = row.find_element_by_xpath('.//div[contains(@class, "event-bets")]')
        list_odds.append(odds.text)
        home = row.find_element_by_xpath('.//div/p[@class="title team"][1]')
        away = row.find_element_by_xpath('.//p[@class="title team"][2]')
        teams.append(home.text + '\n' + away.text)

    driver.quit()
    return list_odds, teams

def store_odds(teams, btts):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    dict_gambling = {'Teams':teams,'btts': btts}
    df_betfair = pd.DataFrame(dict_gambling)

    df_betfair = df_betfair.fillna('')
    df_betfair = df_betfair.replace('CLOSED\n', '', regex=True)
    df_betfair = df_betfair.replace('SUSPENDED\n', '', regex=True)
    df_betfair = df_betfair.applymap(lambda x: x.strip() if isinstance(x, str) else x) #14.0\n

    #save file
    output = open('df_betfair', 'wb')
    pickle.dump(df_betfair, output)
    output.close()
    df_betfair.head()

    betfair_odds = []
    for team, odds in zip(dict_gambling['Teams'], dict_gambling['btts']):
        betfair_odds.append({
            'Team': team,
            'Odds': odds
        })
    return betfair_odds




