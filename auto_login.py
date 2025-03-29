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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B8D87DCF380A0DA2A5FADE57DFE59108DD3F6CBF78935F26FA1D13D4DE5A5F3051A1284534B60E7969B3161CAB0CE967B7AFECC7ED057CC4C749CD7A0EF89075F26B5AC85C8694654DD73B71643230DD9454C768196403A54463EA84C5691CC398AE9EBCD2301631CBE38D43132545D2268F17BDD9DA15BC9822C69AE30839D16C7E85389C4A661C2F9C16A9CA5DA1476387D22E4249A48E158B6BE7C56685D99C8756BA299C0E6F581E5847302D828BD4C7590F89057DDB70006D75571C12C41CD27EE76C43AC7AB5B161873DEC5830EB18BFCB1817FDCAE65BCB2E7339BE87571D15681AFCBCCCFDCE0BF6255919F3056E3F01EF45D186473A1D4578E6A31D854189A232264B8CE2E066694100429F9E6B68E8859287ECF48E341144D1453B75F0CA1F77A486ABD9C749F29489CE5F5674538B4F65D056F7552BDA2EC0F4C7F2B4B636746903BBCCB6412747275F72FB4FC3251AAC6B5F7FFE75EC2FA3F18C"})
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
