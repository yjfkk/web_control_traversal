#coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_fullpage_screenshot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.19lou.com/")
    time.sleep(2)

    #the element with longest height on page
    ele=driver.find_element("xpath", '//*[@id="logo"]/h1/a/img')
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height)  #the trick
    time.sleep(2)
    driver.save_screenshot("screenshot1.png")
    driver.quit()

if __name__ == "__main__":
    test_fullpage_screenshot()