import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def take_screenshot(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, service_log_path=os.devnull)
    full_url = 'http://' + url
    driver.get(full_url)
    driver.save_screenshot(os.getcwd()+'/media/screenshots/{}.png'.format(url))

take_screenshot('google.com')