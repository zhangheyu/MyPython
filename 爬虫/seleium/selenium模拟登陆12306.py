from selenium import webdriver
from time import sleep
from PIL import Image
import requests
from hashlib import md5
from selenium.webdriver import ActionChains

class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    bro = webdriver.Chrome('./chromedriver.exe')
    bro.get('https://kyfw.12306.cn/otn//login/init')
    # 全屏截图，以免截图不全
    bro.maximize_window()
    # 截图保存当前界面用于截取验证码区域
    bro.get_screenshot_as_file('12306.png')
    sleep(2)
    # 确定验证码图片区域的左上角和右下角坐标
    code_image_ele = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')
    # print(code_image_ele)
    location = code_image_ele.location  # 验证码图片的左上角坐标
    print(f'location: {location}')
    size = code_image_ele.size  # 验证码图片标签对应的长和宽
    print(f'size: {size}')
    # 浏览器是按照缩放100%截图的，因此电脑必须也是分辨率100%，不然截图不准！！！！！！！！！！！！
    # 笔记本设置的125%缩放显示！！！！！！！！！！！！！！！！
    rangle = (location['x'], location['y'],
              location['x'] + size['width'], location['y'] + size['height'])
    print(f'rangle: {rangle}')
    fd = Image.open('./12306.png')
    # crop根据指定区域对图片进行裁剪
    frame = fd.crop(rangle)
    code_name = './code.png'
    frame.save(code_name)

    # 价格验证码图片给超级鹰识别
    chaojiying = Chaojiying_Client('zhangheyu', 'zhangheyu', '911090')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    # print(chaojiying.PostPic(im, 9004)['pic_str'])
    result = chaojiying.PostPic(im, 9004)['pic_str']
    print(f'result:{result}')
    all_list = []  # 存储即将被点击的所有坐标[[x1,y1][x2,y2]]
    if '|' in result:
        list1 = result.split('|')
        count1 = len(list1)
        print(f'count1:{count1}, list1:{list1}')
        for i in range(count1):
            xy_list = []
            x = int(list1[i].split(',')[0])
            y = int(list1[i].split(',')[1])
            xy_list.append(x)
            xy_list.append(y)
            all_list.append(xy_list)
    else:
        xy_list = []
        x = int(result.split(',')[0])
        y = int(result.split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
    print(f'all_list:{all_list}')

    # 遍历列表，使用动作链对每一个列表元素对应的xy指定的位置进行操作
    for l in all_list:
        x = l[0]
        y = l[1]
        ActionChains(bro).move_to_element_with_offset(code_image_ele, x, y).click().perform()
        sleep(0.5)
    bro.find_element_by_id('username').send_keys('zzzzzz')
    bro.find_element_by_id('password').send_keys('yyyyy')
    bro.find_element_by_id('loginSub').click()
    sleep(3)
    bro.quit()