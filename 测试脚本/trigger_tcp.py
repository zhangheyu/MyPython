import socket
import json
from ctypes import create_string_buffer
import struct
from time import sleep

ip = '192.168.112.92'
port = 8131

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((ip, port))

def tcp_send_msg_base(cmd_data):
    """
    function:发送tcp命令
    :param cmd_data:
    :return:
    """
    # tcp_client = tcp_client
    global tcp_client
    cmd_len = len(cmd_data)
    # init all \x00
    buf = create_string_buffer(cmd_len + 8)
    struct.pack_into(">2B", buf, 0, 86, 90)  # 'VZ'
    struct.pack_into(">I", buf, 4, cmd_len)
    struct.pack_into(">" + str(cmd_len) + "s", buf, 8, cmd_data)

    try:
        tcp_client.sendall(buf)
    except Exception as err:
        # print('发送异常{}'.format(traceback.format_exc()))
        print('send error')
        # raise
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((ip, port))

while True:
    cmd_string_data = '{"cmd":"trigger"}'
    # 发送命令
    tcp_send_msg_base(cmd_string_data.encode())
    print('send success')
    sleep(2)

tcp_client.close()
