from socket import *
# 创建UDP套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)
# 绑定一个端口
# 绑定的是本机，端口是8888
udp_socket.bind(('', 8888))

while True:
    # 表示本次接收的最大字节数1024
    recv_data = udp_socket.recvfrom(1024)
    msg = recv_data[0].decode('utf-8')
    print(f'接收到%s的消息是：\n %s'%(recv_data[1], msg))
    if msg == 'exit':
        print('再见，程序退出')
        break

# 关闭套接字
udp_socket.close()
