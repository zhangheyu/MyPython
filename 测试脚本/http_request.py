import requests
import json
import time


def get_parking_area_cfg(headers, url):
    get_parking_area_cfg = {
        "type": "get_parking_area_cfg",
        "module": "ALG_REQUEST_MESSAGE"
    }
    json_str = json.dumps(get_parking_area_cfg)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'get_parking_area_cfg:', response.text)


def get_another_device_cfg(headers, url):
    get_another_device_cfg = {
        "type": "get_another_device_ip",
        "module": "SERIAL_COMM_MSG"
    }
    json_str = json.dumps(get_another_device_cfg)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'get_another_device_cfg:', response.text)


def get_backup_http_server(headers, url):
    get_backup_http_server = {
        "type": "get_backup_http_server",
        "module": "BUS_REQUEST_MESSAGE"
    }
    json_str = json.dumps(get_backup_http_server)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'get_backup_http_server:', response.text)


def set_backup_http_server(headers, url):
    set_backup_http_server = {
        "type": "set_backup_http_server",
        "module": "BUS_REQUEST_MESSAGE",
        "body": {
            "server_addr": "192.168.10.10",
            "port": 8888,
            "timeout": 2,
            "push_enable": 1,
            "backup_server_enable": 1,
            "smallimage_enable": 1,
            "bigimage_enable": 1,
            "push_addr": "/F2PlateRecognitionResult/backup/alg"
        }
    }
    json_str = json.dumps(set_backup_http_server)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'set_backup_http_server:', response.text)


def set_dev_led(headers, url):
    for led_id in range(8):
        set_dev_led = {
            "type": "set_dev_led",
            "module": "EVS_BUS_REQUEST",
            "body": {
                "led": led_id
            }
        }
        json_str = json.dumps(set_dev_led)
        response = requests.request("POST", url, headers=headers, data=json_str)
        print(f'set_dev_led {led_id}:', response.text)
        time.sleep(5)


def set_camera_mode_cfg(headers, url):
    set_camera_mode_cfg = {
        "type": "set_camera_mode_cfg",
        "module": "BUS_REQUEST_MESSAGE",
        "body": {
            "camera_mode": 0,
            "enable_extern": 1
        }
    }
    json_str = json.dumps(set_camera_mode_cfg)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'set_camera_mode_cfg:', response.text)


def get_camera_mode_cfg(headers, url):
    get_camera_mode_cfg = {
        "type": "get_camera_mode_cfg",
        "module": "BUS_REQUEST_MESSAGE"
    }
    json_str = json.dumps(get_camera_mode_cfg)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'get_camera_mode_cfg:', response.text)


def get_external_led_status(headers, url):
    get_external_led_status = {
        "type": "get_external_led_status",
        "module": "BUS_REQUEST_MESSAGE"
    }
    json_str = json.dumps(get_external_led_status)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'get_external_led_status:', response.text)


def set_external_control_framestatus(headers):
    url = "http://192.168.104.243/external_control_message.php"
    # "192.168.112.205/external_control_message.php"
    frame_status = {
        "type": "external_control_framestatus",
        "module": "BUS_EXT_REQUEST_MESSAGE",
        "body": {
            "ip": "192.168.6.188",
            "type": "external_control_framestatus",
            "body": {
                "frame_status": [1, 1, 1]
            }
        }
    }
    json_str = json.dumps(frame_status)
    response = requests.request("POST", url, headers=headers, data=json_str)
    print(f'set_external_control_framestatus:', response.text)


def set_dev_led():
    url = "http://192.168.104.201/bus_request_message.php"
    data = {
        "type": "set_dev_led",
        "module": "EVS_BUS_REQUEST",
        "body": {
            "led": 0
        }
    }
    json_str = json.dumps(data)
    response = requests.request("POST", url, data=json_str)
    print(f'set_dev_led:', response.text)

def get_current_image():
    url = "http://192.168.104.201/html/img/result_0.jpg"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    response = requests.request("GET", url, headers=headers)
    # print(f'get_current_image:', response)
    print(response.text)
    print(response.status_code)


def get_plate_result():
    url = "http://192.168.104.4/get_plate_result_poll.php"
    response = requests.request("GET", url)
    str_obj = response.content.decode()
    json_obj = json.loads(str_obj)
    plateresult = json_obj["parkingresult"]["plateresult"]
    format_result = json.dumps(plateresult, sort_keys=True, indent=2)
    print(format_result)


def get_new_energy_plate_support():
    url = "http://192.168.118.206/avsjson.php"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "remember=1; sessionID=1609955606a533958471; outtext=loj1X3t7e3vNS0RBzFa6Lxx1dw%3D%3D",
        "Host": "192.168.118.206",
        "Origin": "http://192.168.118.206",
        "Pragma": "no-cache",
        "Referer": "http://192.168.118.206/login.htm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    get_new_energy_plate_support = {
        "type": "get_new_energy_plate_support"
    }

    json_str = json.dumps(get_new_energy_plate_support)
    print(json_str)
    response = requests.request("GET", url, headers=headers, data=json_str)
    print('get_new_energy_plate_support:', response.content, response.status_code)


def avs_trigger_r2():
    # url = "http://192.168.118.206/avstrigger.php"
    url = "http://192.168.109.223/avstrigger.php"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "sessionID=1611078794a1652181482; remember=1; outtext=C6wGYJ6enp5KlYlUUfKOjNBG7g%3D%3D",
        "Host": "192.168.109.223",
        # "Origin": "http://192.168.118.206",
        "Pragma": "no-cache",
        "Referer": "Referer: http://192.168.109.223/main.htm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.request("GET", url, headers=headers)
    print('avs_trigger_r2:', response.content)


def login(url):
    # login
    # url = "http://192.168.112.206/request.php"
    login_str = {
        "type": "login",
        "module": "BUS_WEB_REQUEST",
        "user_info": "ZRVbX1xcXFyCh5lv14Kc27A/Sw: ="
    }
    login_json = json.dumps(login_str)
    response = requests.request("POST", url, data=login_json)
    print(response.text)

    sessionID = response.headers['Set-Cookie'].split(';')[0]
    headers = {
        'Cookie': sessionID,
        'Content-Type': 'application/json'
    }
    return headers


# get_parking_area_cfg(headers, request_url)
# get_another_device_cfg(headers,request_url)

# set_backup_http_server(headers, request_url)
# get_backup_http_server(headers, request_url)

if __name__ == '__main__':
    request_url = "http://192.168.104.199/request.php"
    # headers = login(request_url)
    # get_backup_http_server(headers, request_url)
    # set_dev_led(headers, request_url)
    # set_camera_mode_cfg(headers, request_url)
    # get_camera_mode_cfg(headers, request_url)
    # get_external_led_status(headers, request_url)
    # set_external_control_framestatus(headers)
    # get_current_image()
    get_plate_result()
    # get_new_energy_plate_support()
    # while True :
    #     avs_trigger_r2()
    #     time.sleep(2)
    # set_dev_led()
