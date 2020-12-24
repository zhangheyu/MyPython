from selenium import webdriver
from time import sleep

if __name__ == '__main__':
    bro = webdriver.Chrome('./chromedriver.exe')
    bro.get('https://i.qq.com/')
    # 登录选项(用户名密码/注册账户)位于iframe内
    bro.switch_to.frame('login_frame')
    # id="switcher_plogin" 账户密码登录
    login_btn = bro.find_element_by_id('switcher_plogin')
    login_btn.click()
    sleep(2)
    user_tag = bro.find_element_by_id('u')
    passwd_tag = bro.find_element_by_id('p')
    user_tag.send_keys('1371542956')
    sleep(1)
    passwd_tag.send_keys('261219zhy')
    sleep(1)
    button_login = bro.find_element_by_id('login_button')
    button_login.click()
    sleep(20)
    bro.quit()
