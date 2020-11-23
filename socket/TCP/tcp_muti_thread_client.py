from socket import *
from threading import Thread

flag = True


def readMsg(client_socket):
    print('接收线程启动')
    while flag:
        recv_data = client_socket.recv(1024)
        print(f'收到', recv_data.decode('utf-8'))
    print('接收线程结束')

def writeMsg(client_socket):
    print('发送线程启动')
    global flag
    while flag:
        msg = input('>')
        msg = user_name + '说：' + msg
        client_socket.send(msg.encode('utf-8'))
        # 如果输入bye时候下线
        if msg.endswith('bye'):
            flag = False
            break
    print('发送线程结束')

# 创建客户端套接字对象
client_socket = socket(AF_INET, SOCK_STREAM)
# 调用connect连接服务器
client_socket.connect(('192.168.31.237', 8888))
user_name = input('请输入用户名：')
# 开启一个线程处理客户端的读取消息
t1 = Thread(target=readMsg, args=(client_socket,))
t1.start()
# 开启一个线程处理客户端的发送消息
t2 = Thread(target=writeMsg, args=(client_socket,))
t2.start()
t1.join()
t2.join()
client_socket.close()
print('主进程退出')