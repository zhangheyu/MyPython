from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 实现无可视化界面
from selenium.webdriver import ChromeOptions  # 实现规避检测
from time import sleep

if __name__ == '__main__':
    # 实现无可视化界面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实现规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options, options=option)
    driver.get("http://www.baidu.com")
    # print(driver.page_source)
    driver.close()
