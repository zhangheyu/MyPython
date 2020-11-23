from socket import AF_INET, SOCK_DGRAM, socket
udp_socket = socket(AF_INET, SOCK_DGRAM)
addr = ('192.168.31.237', 9999)

while True:
    data = input('请输入要发送信息：')
    udp_socket.sendto(data.encode('utf-8'), addr)
    if data == 'exit':
        print('程序退出')
        break

udp_socket.close()
