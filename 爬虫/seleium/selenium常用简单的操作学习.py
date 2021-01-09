from selenium import webdriver
from time import sleep

if __name__ == '__main__':
    bro = webdriver.Chrome(executable_path='./chromedriver.exe')
    bro.get('https://www.taobao.com/')
    # 标签定位
    search_input = bro.find_element_by_id('q')
    # 标签交互
    # send_keys 输入文本信息
    search_input.send_keys('飞机')
    # 点击搜素按钮
    search_submit = bro.find_element_by_css_selector('.btn-search')
    # click 点击元素
    search_submit.click()
    sleep(2)
    # 执行js脚本程序
    bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    bro.get('https://www.baidu.com')
    sleep(2)
    # 回退
    bro.back()
    sleep(2)
    # 前进
    bro.forward()
    # 百度搜索
    input_bd = bro.find_element_by_class_name('s_ipt')
    input_bd.send_keys('飞机')
    su = bro.find_element_by_id('su')
    su.click()
    sleep(2)
    # 向下滚动
    bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(5)
    # clear 清除文本信息（上次发送的文本信息）
    input_bd.clear()
    input_bd.send_keys('大炮')
    su.click()
    # 浏览器窗口最大化
    bro.maximize_window()
    # 提交（回车）
    input_bd.clear()
    input_bd.send_keys('yoyo')
    su.submit()
    # 刷新页面
    bro.refresh()
    sleep(2)
    # 截取当前窗口，并指定截图图片的保存位置
    # bro.get_screenshot_as_file("baidu_img.jpg")
    sleep(5)
    bro.quit()
