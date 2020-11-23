from socket import *

# 创建客户端套接字对象
client_socket = socket(AF_INET, SOCK_STREAM)
# 调用connect方法与服务器建立连接
client_socket.connect(('192.168.31.237', 8888))
while True:
    # 客户端发送消息
    msg = input('>')
    client_socket.send(msg.encode('utf-8'))
    if msg == 'bye':
        break
    # 客户端接收消息
    recv_data = client_socket.recv(1024)
    print(f'服务器端说：', recv_data.decode('utf-8'))
client_socket.close()
