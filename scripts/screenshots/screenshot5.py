from selenium import webdriver
from PIL import Image
import os
from webdriver_manager.chrome import ChromeDriverManager

file_path = os.path.realpath(__file__)
driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.google.com/"
driver.get(url)
driver.save_screenshot('target.png')
screenshot = Image.open('target.png')
screenshot.show()