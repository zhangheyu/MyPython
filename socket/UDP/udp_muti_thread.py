from socket import *
from threading import Thread

# 创建UDP套接字对象
udp_socket = socket(AF_INET, SOCK_DGRAM)
# 绑定本机和端口
udp_socket.bind(('', 9999))


# 接收
def my_recv():
    print('接收线程启动')
    while True:
        # 表示本次接收的最大字节数1024
        recv_data = udp_socket.recvfrom(1024)
        msg = recv_data[0].decode('utf-8')
        print(f'接收到%s的消息是：\n %s' % (recv_data[1], msg))
        if msg == 'exit':
            break
    print('再见，接收线程退出')
    return


# 发送
def my_send():
    print('发送线程启动')
    addr = ('192.168.31.237', 8888)
    while True:
        data = input('请输入要发送信息：')
        udp_socket.sendto(data.encode('utf-8'), addr)
        if data == 'exit':
            break
    print('发送线程退出')
    return


if __name__ == '__main__':
    # 创建两个线程
    t1 = Thread(target=my_send)
    t2 = Thread(target=my_recv)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    udp_socket.close()
    print('进程退出')
