import struct
from socket import *

filename = 'beauty.jpg'
server_ip = '127.0.0.1'
# 封装读请求
send_data = struct.pack('!H%dsb5sb' % len(filename), 1, filename.encode(), 0, 'octet'.encode(), 0)
# 创建udp_socket套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.sendto(send_data, (server_ip, 69))  # 读写端口默认是69
# 本地创建一个文件
f = open(filename, 'ab')  # a追加模式  b二进制
while True:
    recv_data = udp_socket.recvfrom(1024)
    # print(recv_data) ('19\x1a&\'()*56789:CDEFGHI', ('127.0.0.1', 63568))
    # 获取操作码及数据块编号
    operation_code, ack_num = struct.unpack('!HH', recv_data[0][:4])
    # 判断操作码是否是5如果是5，则是错误信息
    if operation_code == 5:
        print('文件不存在')
        break
    # 将接收到的数据写入到文件中
    f.write(recv_data[0][4:])
    if len(recv_data[0]) < 516:  # 表示读取完
        break
    # 发送确认包
    ack_data = struct.pack('!HH', 4, ack_num)
    rand_port = recv_data[1][1]  # 获取服务器发送数据的随机端口
    udp_socket.sendto(ack_data, (server_ip, rand_port))
