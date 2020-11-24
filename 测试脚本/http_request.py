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
    headers = login(request_url)
    # get_backup_http_server(headers, request_url)
    # set_dev_led(headers, request_url)
    # set_camera_mode_cfg(headers, request_url)
    # get_camera_mode_cfg(headers, request_url)
    # get_external_led_status(headers, request_url)
    set_external_control_framestatus(headers)
