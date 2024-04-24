from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import os

print("\033cmonkeytype-hack by @p55d2k")

options = Options()
options.add_argument("--log-level=3")

print("Opening browser...")
driver = webdriver.Chrome(options=options)
driver.get("https://monkeytype.com/")
driver.maximize_window()

actions = ActionChains(driver)
time.sleep(1)

try:
    driver.find_element("xpath", '//*[@id="cookiesModal"]/div[2]/div[2]/div[2]/button[1]').click()
except:
    print("\"Accept Cookies\" popup not found. Press \"accept all\", then press enter back in the terminal once you have done so.")
    input()
    time.sleep(1.5)

print("Starting typing test...")
time.sleep(1.5)

starttime = time.time()
times = []

while True:
    wordtime = time.time()

    word = driver.find_element(By.CSS_SELECTOR, "#words > div.word.active").text
    actions.send_keys(word + " ")
    actions.perform()

    times.append(time.time() - wordtime)

    if time.time() - starttime > 30:
        break

time.sleep(10)
wpm = driver.find_element("xpath", '//*[@id="result"]/div[1]/div[1]/div[2]').text

if wpm == "Infinite":
    wpm = driver.find_element("xpath", '//*[@id="result"]/div[2]/div[3]/div[2]').text

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists("screenshots"):
    os.mkdir("screenshots")

driver.save_screenshot("screenshots/" + wpm + "_wpm.png")

if not os.path.exists("logs.txt"):
    with open("logs.txt", "w") as f:
        f.write("")

average_word_time = round(sum(times) / len(times), 3)
fastest_word_time = round(min(times), 3)
slowest_word_time = round(max(times), 3)

with open("logs.txt", "a") as f:
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {wpm} WPM\n")
    f.write(f"Average word time: {average_word_time}\n")
    f.write(f"Fastest word time: {fastest_word_time}\n")
    f.write(f"Slowest word time: {slowest_word_time}\n")
    f.write("\n")

print(f"\nFinished typing test.\nWPM: {wpm}\nAverage word time: {average_word_time}\nFastest word time: {fastest_word_time}\nSlowest word time: {slowest_word_time}\n\nScreenshot saved as {wpm}_wpm.png in the screenshots folder\nLogs saved in logs.txt")
driver.quit()
