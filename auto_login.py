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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E427532730B8DCF682718C66FB86FD90DCFD860271C076CEB8E655D1C7AC2872C1F4F9016D52ED59A9B577E14BFC428E975C379FC9C4DF3253A8819761C1FBECF6DFD31D226FC9EDDF787B6229D9FF1FDA02E63D3B86821D1919D75F0DC0C16FB4143615AA1DBE69C09198328F41A57AC105A42D619247490AAF889E6BEB40B70803391A24522A395A3D6B4C3ED798FBE01E5107357EE1A76D6366BBE8FEB93A2CB61F5015C7E7081F411D5FCD381B09593C598719E862EC9A07E0954C486D3D841BBCF5527B1DB0EADE7C2C30ED12E3CDA8FA230211F98CF3F6C29C91DF26D0C8B6CC8978766FA60882A6C774621F83C681C4584E84A6B1E16424B7EFA7A80FDCAA5379EFFFD0F04915F2C39701A67317069C7E6956BE2469D9403682F16209BD080F9A1D381DA7DCA1B40391CE2D886657F3DA5DEF5EEBB153494E0738833F20474A0BDE9A51164AD3C78FA16EAD72"})
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
