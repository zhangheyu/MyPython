from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep

if __name__ == '__main__':
    bro = webdriver.Chrome('./chromedriver.exe')
    bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
    # driver.switch_to.frame(reference)  # 切到指定frame，可用id或name(str)、index(int)、元素(WebElement)定位
    # driver.switch_to.parent_frame()  # 切到父级frame，如果已是主文档，则无效果
    # driver.switch_to.default_content()  # 切到主文档，DOM树最开始的<html>标签
    # 如果要定位的标签位于iframe标签之中则必须按照如下操作进行标签定位
    bro.switch_to.frame('iframeResult')  # 切换浏览器标签定位的作用域
    div = bro.find_element_by_id('draggable')
    print(div)
    # 动作链
    action = ActionChains(bro)
    # 点击长安指定的标签
    action.click_and_hold(div)
    for i in range(5):
        # perform立即执行动作链操作
        # move_by_offset(x, y) x=横坐标， y=纵坐标
        action.move_by_offset(18, 0).perform()
        sleep(0.3)
    # 从iframe中切回主文档，继续对主文档进行分析处理
    bro.switch_to.default_content()

    # 释放动作链
    action.release()
    sleep(5)
    bro.quit()

