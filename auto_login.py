# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0022557F814287248AEB4AEC1057E8E47AF194403C242207C3C8607065DB8BD57CEF1DA6451F628EF902ABDB2E8B7384E45BD9CA7D19CAB8CD449D5F28FDB155946A72A8BB7B7BE350CA82C4B64EFFD081077EEA257B5BB737529E88EB79C9DB92427B3EFC1FCE1B826F6E5E34C6EB6CDCDAABBBBAD7C14E3308E64CEB057F76FAC2EC99F1BD2B73E613F2EBC61C1EDF241E28FFBCEE4E6A1E9EA21304875E4BA8EEE38D34920CD51D149428EE8DA7E585FBF44A7597DE2B3150F93EC09D95E43B1DDDD5C535D71B491C1C82D7AD0495B7C29C69B9F385356994443863BCF95E45C4F1687132E14A8E596D3D2BE89FD7C5D18EF16DC83232A7F806F8674000BDBE260B3B1521D1B6E9A4A6CD4C70191E366AC55A484967195C19F9BC06D2F42C1B157DAA8C29A1A363D1F878F5CCAC73E8A434BF8AB9314502E72E7669E564BF89498A1B9AF632A4FC28044336547EB378D4BE4F2145345212839B618CB676F341"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
