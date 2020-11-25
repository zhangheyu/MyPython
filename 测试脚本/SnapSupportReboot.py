# encoding=utf-8
# 'desc：手动抓拍测试工具
# 'author: yuyang by 2018-12-14

import os
import sys
import socket
import json
import struct
import base64
import threading
from ctypes import create_string_buffer
from time import ctime, sleep, strftime, localtime

g_dev_ip_list = [
    # '192.168.6.114',
    '192.168.112.92'
]


def AddDevIp(*ip_addr):
    for ip in ip_addr:
        g_dev_ip_list.append(ip)


##参数配置区开始########################################    
# 1、填写开启手动抓拍设备的IP地址,IP参数可填一个或多个
# AddDevIp('192.168.109.90', '172.16.0.91', '172.16.0.80', '192.168.109.83', '192.168.109.84', '192.168.109.23')

# g_dev_ip_list.append('192.168.116.118')
# g_dev_ip_list.append('192.168.116.116')
# 2、填写触发抓拍的间隔时间，单位“秒”
g_snap_interval = 1
# 3、是否打开设备异常重启后继续触发的功能
g_support_reboot = True
##参数配置区结束########################################

TCP_PORT = 8132
g_socket_array = {}
g_socket_error_array = {}
g_tcp_client = []
g_fd = []
g_reboot_iplist = []
g_all_threads_over = False
g_is_print = False


# 触发设备手动抓拍
def trigger_result():
    cmd_data = '{ "type" : "avs_trigger","id" : 123456,"module" : "AVS_REQUEST_MESSAGE","user_info" : "eun1XEtLS0uUuJTtaJUAugBj4A==","block_flag" : 1,"body":{"trigger_result":1,"trigger_type":0}}'
    # cmd_data = '{"type":"avs_trigger","module":"AVS_REQUEST_MESSAGE","body":{"trigger_result":1,"trigger_type":0}}'
    # cmd_data= '{"cmd":"trigger"}'
    for tcp_client in g_tcp_client:
        send_msg(tcp_client, cmd_data.encode())


def get_dev_id(socket):
    return g_socket_array[hash(socket)]


# 初始并建立化TCP连接
def start_tcp_client(ip_list):
    global g_tcp_client
    global tcp_client

    for server_ip in ip_list:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect((server_ip, TCP_PORT))
        except socket.error:
            print('Fail to setup socket connection.')
            tcp_client.close()

        g_socket_array[hash(tcp_client)] = server_ip
        g_socket_error_array[hash(tcp_client)] = 0
        g_tcp_client.append(tcp_client)

        print(" [%-16s] start to capturing every %s seconds." % (server_ip, g_snap_interval))


# 添加单个TCP连接
def StartOneTcpClient(server_ip):
    global g_tcp_client
    global tcp_client

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((server_ip, TCP_PORT))
    except socket.error:
        print('Fail to setup socket connection.')
        tcp_client.close()

    g_socket_array[hash(tcp_client)] = server_ip
    g_socket_error_array[hash(tcp_client)] = 0
    g_tcp_client.append(tcp_client)
    g_reboot_iplist.remove(get_dev_id(tcp_client))
    print(" [%-16s] start to capturing every %s seconds." % (server_ip, g_snap_interval))


# 关闭TCP连接
def close_tcp_client():
    global g_tcp_client

    try:
        for mysocket in g_tcp_client:
            mysocket.close()
    except socket.error:
        print('Fail to close socket connection.')


# 从TCP连接上面接收数据
def recv_tcp_data():
    global g_tcp_client
    global g_all_threads_over

    while (g_all_threads_over == False):
        for tcp_client in g_tcp_client:
            try:
                response = tcp_client.recv(8)
                if (b'VZ' == response[0:2]):
                    data_len = struct.unpack('>i', bytes(response[4:8]))
                    # print("Recv data len:", data_len[0]);
                    response = tcp_client.recv(data_len[0])

                    if (response == b''):  # 心跳包返回空字串
                        continue

                    g_fd[1].write("[%s]Recv %-16s response data:%s\n" % (
                        strftime("%Y-%m-%d %H:%M:%S", localtime()), get_dev_id(tcp_client), response))
                    g_fd[1].flush()
                    if g_is_print:
                        print("[%s]Recv %-16s response data:%s\n" % (
                            strftime("%Y-%m-%d %H:%M:%S", localtime()), get_dev_id(tcp_client), response))

                    # 解析数据
                    # parse_json(response);
                else:
                    response = tcp_client.recv(1024)

            except socket.error:
                print('Fail to recv socket connection for %s.\n' % get_dev_id(tcp_client))

    print("recv_tcp_data thread is exit!\n")


# 向TCP连接上发送数据        
def send_msg(mysocket, cmd_data):
    global g_tcp_client
    global g_reboot_iplist
    cmd_len = len(cmd_data)

    g_fd[0].write(
        "[%s]send %s to %s \n" % (strftime("%Y-%m-%d %H:%M:%S", localtime()), cmd_data, get_dev_id(mysocket)))
    g_fd[0].flush()
    # print(cmd_data)
    if g_is_print:
        print('%s send to %s success.\n' % (cmd_data, get_dev_id(mysocket)))

    # init all \x00
    buf = create_string_buffer(cmd_len + 8)
    struct.pack_into(">2B", buf, 0, 86, 90)  # 'VZ'
    struct.pack_into(">I", buf, 4, cmd_len)
    struct.pack_into(">" + str(cmd_len) + "s", buf, 8, cmd_data)

    try:
        mysocket.sendall(buf)
    except socket.error:
        print('%s send to %s failed.\n' % (cmd_data, get_dev_id(mysocket)))
        g_socket_error_array[hash(mysocket)] += 1
        if (g_socket_error_array[hash(mysocket)] > 1):
            g_tcp_client.remove(mysocket)
            g_reboot_iplist.append(get_dev_id(mysocket))


# 发送心跳包
def send_heartbeat_message_proc():
    global g_tcp_client
    global g_all_threads_over

    buf = create_string_buffer(8)
    struct.pack_into(">2B", buf, 0, 86, 90)
    struct.pack_into(">B", buf, 2, 1)  # 0x01
    struct.pack_into(">I", buf, 4, 0)

    while (g_all_threads_over == False):
        sleep(9)
        for tcp_client in g_tcp_client:
            try:
                tcp_client.sendall(buf)
                # print("Send heartbeat message.");
            except socket.error:
                print('Send heartbeat message failed.\n')
                break
    print("send_heartbeat_message_proc thread is exit!\n")


# 线程创建处理函数    
def create_thread():
    global g_all_threads_over

    mythreads = []
    # 初始化线程运行标志
    g_all_threads_over = False

    t1 = threading.Thread(target=recv_tcp_data, args=())
    mythreads.append(t1)
    t2 = threading.Thread(target=send_heartbeat_message_proc, args=())
    mythreads.append(t2)

    for t in mythreads:
        t.setDaemon(True)
        t.start()
    sleep(1)


# 销毁所有的线程
def destroy_thread():
    global g_all_threads_over
    g_all_threads_over = True
    sleep(11)
    print("All threads over!\n")


# 创建日志文件
def create_logfile():
    global g_fd
    g_fd.append(open('send.txt', 'w'))
    g_fd.append(open('recv.txt', 'w'))


# 关闭日志文件
def close_logfile():
    global g_fd
    for fd in g_fd:
        fd.close()


# 解析json数据
def parse_json(json_str):
    # b'{"cmd" : "ttransmission","subcmd" : "send","comm" : 0,"datalen" : 10,"data" : "MTIzNDU2Nzg5MA=="}\x00'
    json_array = json_str.decode('utf-8').rstrip('\x00')
    json_dict = json.loads(str(json_array))

    if ('ttransmission' == str(json_dict['cmd'])
            and 'send' == str(json_dict['subcmd'])
            and ('data' in json_dict)):
        datalen = json_dict['datalen']
        recv_data = base64.b64decode(json_dict['data'])


def snap_test():
    global g_dev_ip_list
    start_tcp_client(g_dev_ip_list)
    create_thread()

    # 测试执行
    while (True):
        trigger_result()
        sleep(g_snap_interval)
        reconnect_tcp()

    destroy_thread()
    close_tcp_client()


def do_ping(host):
    ret = os.system('ping -n 2 -w 1 %s' % host)
    if ret:
        # print ('ping %s is fail'%host);
        return False
    else:
        # print ('ping %s is ok'%host);
        return True


def reconnect_tcp():
    if g_support_reboot:
        for IpAddr in g_reboot_iplist:
            if do_ping(IpAddr):
                StartOneTcpClient(IpAddr)


if __name__ == "__main__":
    create_logfile()
    snap_test()
    close_logfile()
    print('hello')
