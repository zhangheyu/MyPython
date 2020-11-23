import requests
import json

while True:
    your_chat = input('你说：')  # 假定为  ： 你是谁？
    # url: 机器人接口地址
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    # data_param: post请求的参数，向服务器提交的数据。类型为字典(dict)
    # inputeText ----> text:你的聊天信息（一句话）
    data_param = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": your_chat
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "成都",
                    "province": "四川",
                    "street": "12222"
                }
            }
        },
        "userInfo": {
            "apiKey": "dab5372cc7824055bcebb9814609dfe2",
            "userId": "669959"
        }
    }
    response = requests.post(url=url, json=data_param)
    py_json = response.text

    py_dict = json.loads(py_json)
    results_list = py_dict['results']
    results_0_dict = results_list[0]
    values_dict = results_0_dict['values']
    text_str = values_dict['text']
    print('图灵说：' + text_str)
