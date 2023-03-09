from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

url = "https://u.gg/lol/tier-list"

options = Options()
options.add_argument("--headless") # Run Chrome in headless mode
service = Service("chromedriver.exe") # Path to your Chromedriver executable
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

file = open("Tierlist.csv", 'w')
writer = csv.writer(file)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.rt-tr-group")))

champions = []
win_rates = []
pick_rates = []

writer.writerow(['Champion Name', 'Win rate', 'Pick Rate'])

while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    # Scroll back to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    # Check if all rows have been loaded
    rows = driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")
    if len(rows) == len(champions):
        break
    
    # Otherwise, continue to extract the data
    for i in range(len(champions), len(rows)):
        row = rows[i]
        champion = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(3)").get_attribute("textContent")
        win_rate = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(5)").text.strip()
        pick_rate = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(6)").text.strip()
            
        champions.append(champion)
        win_rates.append(win_rate)
        pick_rates.append(pick_rate)

        writer.writerow([champion, win_rate, pick_rate])

print(champions)
print(win_rates)
print(pick_rates)

driver.quit()
