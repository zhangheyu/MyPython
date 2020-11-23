from socket import *

# 创建服务器端套接字对象
server_socket = socket(AF_INET, SOCK_STREAM)
# 绑定端口
server_socket.bind(('', 8888))
# 监听
server_socket.listen()
# 等待客户端的连接
client_socket, client_info = server_socket.accept()
while True:
    # 接收客户端的消息
    recv_data = client_socket.recv(1024)
    print(f'客户端说：', recv_data.decode('utf-8'))
    if recv_data.decode('utf-8') == 'bye':
        break
    # 发送消息
    msg = input('>')
    client_socket.send(msg.encode('utf-8'))
client_socket.close()
server_socket.close()
