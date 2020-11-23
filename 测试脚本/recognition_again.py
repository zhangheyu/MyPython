import base64
import socket
import json
from ctypes import create_string_buffer
import struct
import time

ip = '192.168.112.92'
port = 8131
client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_fd.connect((ip, port))

with open('川C640.jpg', 'rb') as f:  # 以二进制读取图片
    data = f.read()
    encodestr = base64.b64encode(data).decode()  # 得到 byte 编码的数据
    # print('data', encodestr)

IMG_INFO = {
    "cmd": "ivs_recognition_again",
    "body": {
             # "image_data": ""
            "image_data": str(encodestr)
        }
    }

GET_IVS = {
    'cmd': 'getivsresult',
    'image': 'false',
    'format': 'json'
}

print('cmd:', IMG_INFO['cmd'])
# print('image_data:', IMG_INFO['body']['image_data'])
img_json = json.dumps(IMG_INFO)
print('send ', img_json)
cmd_data = str(img_json).encode()
cmd_len = len(cmd_data)
buf = create_string_buffer(cmd_len + 8)
struct.pack_into(">2B", buf, 0, 86, 90)  # 'VZ'
struct.pack_into(">I", buf, 4, cmd_len)
struct.pack_into(">" + str(cmd_len) + "s", buf, 8, cmd_data)
print('bufLen:', len(buf))
client_fd.sendall(buf)

time.sleep(0.1)
response = client_fd.recv(20480)
print('response', response.decode())
response = client_fd.recv(20480)
print('response', response.decode())
client_fd.close()
