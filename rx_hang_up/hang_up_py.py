import json
import socket
import telnetlib
import threading
import traceback
from ctypes import create_string_buffer
from time import sleep
import logging
import struct
import select
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
from email.mime.text import MIMEText


dev_version_dics_info = {}  # 升级情况
dev_reboot_err_dic = {}  # 设备重启异常情况
record_raise_err_time = {}  # 记录服务首次异常时间
hang_up_time = None  # 记录挂机时间

tcp_clients_dic = {

}




  # 包含三个方法：attachAttributes()、attachBody()和attachAttachment()，分别用来组装属性、正文和附件。
class MailAssembler:
    def attachAttributes(self,msg,subject,from_name,from_mail,to_mail,cc_mail=None):
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = Header(from_name + " <" + from_mail + ">", "utf-8")
        msg["To"] = Header(",".join(to_mail), "utf-8")
        msg["Cc"] = Header(",".join(cc_mail), "utf-8")

    def attachBody(self,msg,body,type,imgfile=None):
        msgtext = MIMEText(body, type, "utf-8")
        msg.attach(msgtext)

        if imgfile != None:
            try:
                file = open(imgfile, "rb")
                img = MIMEImage(file.read())
                img.add_header("Content-ID", "<image1>")
                msg.attach(img)
            except(Exception) as err:
                print(str(err))
            finally:
                if file in locals():
                    file.close()

    def attachAttachment(self,msg,attfile):
        att = MIMEBase("application", "octet-stream")

        try:
            file = open(attfile, "rb")
            att.set_payload(file.read())
            encoders.encode_base64(att)
        except(Exception) as err:
            print(str(err))
        finally:
            if file in locals():
                file.close()

        if "\\" in attfile:
            list = attfile.split("\\")
            filename = list[len(list) - 1]
        else:
            filename = attfile
        att.add_header("Content-Disposition", "attachment; filename='%s'" %filename)

        msg.attach(att)


# 只有一个sendMail()方法，初始化的时候保存了发送的相关参数，之后就可以用该方法发送其参数msg了。
class MailSender:
    def __init__(self,smtpserver,smtpport,password,from_mail,to_mail,cc_mail=None):
        self.smtpserver = smtpserver
        self.smtpport = smtpport
        self.password = password
        self.from_mail = from_mail
        self.to_mail = to_mail
        self.cc_mail = cc_mail

    def sendMail(self,msg):
        try:
            smtp = smtplib.SMTP_SSL(self.smtpserver, self.smtpport)
            smtp.login(self.from_mail, self.password)
            if self.cc_mail == None:
                smtp.sendmail(self.from_mail, self.to_mail, msg.as_string())
            else:
                smtp.sendmail(self.from_mail, self.to_mail+self.cc_mail, msg.as_string())
            print("执行报告发送 successful")
        except(smtplib.SMTPRecipientsRefused):
            print("Recipient refused")
        except(smtplib.SMTPAuthenticationError):
            print("Auth error")
        except(smtplib.SMTPSenderRefused):
            print("Sender refused")
        except(smtplib.SMTPException) as e:
            print(e.message)
        finally:
            smtp.quit()




def send_email_qq_demo():
    """
    function:demo ，完整的例子，麻雀虽小，五脏俱全
    :return:
    """
    subject = "test report"#主题
    from_name = "agileone项目"#发件人
    from_mail = "578863544@qq.com"#发件人
    to_mail = ["647462724@qq.com","703520848@qq.com"]#收件人
    cc_mail = ["703520848@qq.com"]#抄送
    imgbody = '''
    <h3>hi, the attachment is the test report of this test, please check it in time.</h3>
    <img src="cid:image1"/>
    '''
    file1 = r"..\test\result.html"
    file2 = r"..\test\result.txt"
    imgfile = r"..\test\result.png"

    smtpserver = "smtp.qq.com"
    smtpport = 465
    password = "bamihpoyyumabeai"     # 授权码

    msg = MIMEMultipart()
    assembler = MailAssembler()
    sender = MailSender(smtpserver,smtpport,password,from_mail,to_mail,cc_mail)
    assembler.attachAttributes(msg,subject,from_name,from_mail,to_mail,cc_mail)
    assembler.attachBody(msg,imgbody,"html",imgfile)
    assembler.attachAttachment(msg,file1)
    assembler.attachAttachment(msg,file2)
    sender.sendMail(msg)

def send_email_qq():
    subject = "test report"#主题
    from_name = "agileone项目"#发件人
    from_mail = "578863544@qq.com"#发件人
    to_mail = ["647462724@qq.com","703520848@qq.com"]#收件人
    cc_mail = ["703520848@qq.com"]#抄送
    imgbody = '''
    <h3>anileone用例执行结果报告文件</h3>
    '''
    #获取最后一个文件，根据时间戳
    os.path.dirname(os.getcwd())
    file_dir =os.path.join(os.path.dirname(os.getcwd()),'reports')
    list=os.listdir(file_dir)
    list.sort(key=lambda fn: os.path.getmtime(file_dir+r'\\'+fn) if not os.path.isdir(file_dir+r'\\'+fn) else 0)
    #可以查看获取文件修改时间
    d=datetime.datetime.fromtimestamp(os.path.getmtime(file_dir+r'\\'+list[-1]))
    #待发送文件路径
    send_reports_file = file_dir+r'\\'+list[-1]

    smtpserver = "smtp.qq.com"
    smtpport = 465
    password = "bamihpoyyumabeai"     # 授权码

    msg = MIMEMultipart()
    assembler = MailAssembler()
    sender = MailSender(smtpserver,smtpport,password,from_mail,to_mail,cc_mail)
    assembler.attachAttributes(msg,subject,from_name,from_mail,to_mail,cc_mail)
    assembler.attachBody(msg,imgbody,"html")
    assembler.attachAttachment(msg,send_reports_file)
    sender.sendMail(msg)

def send_email_qq_one(des,subject= '常稳挂机测试反馈'):
    mail_host="smtp.qq.com"       #设置服务器:这个是qq邮箱服务器，直接复制就可以
    mail_pass="svkfdbeygqtxbbag"           #刚才我们获取的授权码
    sender = '647462724@qq.com'      #你的邮箱地址
    receivers = ['578863544@qq.com']  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    content = '{}'.format(des)
    message = MIMEText(content, 'plain', 'utf-8')

    message['From'] = Header("低位常稳挂机", 'utf-8')
    message['To'] =  Header("测试人员", 'utf-8')

    # subject = '常稳挂机测试反馈'  #发送的主题，可自由填写
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(sender,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败')




def tcp_recv_data_common(ip, timeout=2):
    """
    处理接收数据
    break_flag:中断循环标志位
    :return:
    """
    up_client = False  # 更新TCP客户端标志位
    tcp_client = tcp_clients_dic[ip]
    while True:
        try:

            if up_client == True:
                # print('tcp_recv_data_common  更新tcp连接')
                up_client = False  # 重置标志位
                tcp_client = tcp_clients_dic[ip]  # 更新客户端

            # 设置 recv 超时时间
            # ready = select.select([tcp_client], [], [], timeout)
            response = tcp_client.recv(20480)
            # if ready[0]:
                # print('tcp_recv_data_common 已接收到数据....')
                # 接收结果
                # response = tcp_client.recv(2048)
                # print('tcp_recv_data_common {}接收数据 response = {}'.format(ip,response))
        except Exception as err:
            # print('tcp_recv_data_common err {}'.format(traceback.format_exc()))
            up_client = True  # 更新客户端


class BaseLinuxTelent():
    """
    用于操作telent连接的设备
    """

    def __init__(self):
        self.tn = telnetlib.Telnet()

    # 此函数实现telnet登录主机
    def login_host(self, host_ip, username, password):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip, port=23)
        except:
            # log.log_info('%s网络连接失败' % host_ip,write=False)
            # print('%s网络连接失败' % host_ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'login: ', timeout=10)
        self.tn.write(username.encode('ascii') + b'\r\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(password.encode('ascii') + b'\r\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')

        if 'Login incorrect' not in command_result:
            # log.log_info('%s登录成功' % host_ip,write=False)
            return True
        else:
            # log.log_info('{}登录失败，用户名或密码错误'.format(host_ip),write=False)
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self, command):
        """
        直接执行命令
        :param command:
        :return:
        """
        # 执行命令
        self.tn.write(command.encode('ascii') + b'\n')
        sleep(2)
        # 获取命令结果
        command_result = self.tn.read_very_eager().decode('ascii')
        # log.log_info('命令{}执行结果：\n【{}】'.format(command,command_result),write=False)
        return command_result

    def excute_some_command_until(self, command, until):
        """
        :param command:
        :param until: 期待返回值
        :return:
        """
        # 执行命令
        try:
            self.tn.write(command.encode('ascii') + b'\n')
            command_result = self.tn.read_until(until.encode('ascii'), timeout=30)
            command_result = command_result.decode('utf-8')
            start_index = command_result.find('\r\n')
            command_result = command_result[start_index + 2:]
            # 获取命令结果
            # log.log_info('命令执行结果：\n【{}】'.format(command_result))
            return command_result
        except Exception as err:
            # log.log_err("执行命令{}失败".format(command))
            pass

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"exit\n")
        # log.log_info("{}退出登录")


# TCP 通信
class CommonTcpFuns():
    """
    TCP 命令集
    """

    def __init__(self, ip='', port=''):
        if ip == '' or port == '':
            return

        self.ip = ip
        self.tcp_port = port
        self.tcp_start_client()
        # self.tcp_client.setblocking(0)  # 非阻塞模式

    def tcp_start_client(self):
        """
        连接TCP
        :return:
        """
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.tcp_client.connect((self.ip, self.tcp_port))
        except socket.error:
            print('Fail to setup socket connection. err is {}'.format(socket.error))
            self.tcp_client.close()

    def tcp_recv(self, buffer=1024):
        self.tcp_client.recv(buffer)

    def tcp_close_client(self):
        """
        关闭tcp连接
        :return:
        """
        self.tcp_client.close()

    # 向TCP连接上发送数据
    def tcp_send_msg_base(self, cmd_data):
        """
        function:发送tcp命令
        :param cmd_data:
        :return:
        """
        tcp_client = self.tcp_client
        cmd_len = len(cmd_data)
        # init all \x00
        buf = create_string_buffer(cmd_len + 8)
        struct.pack_into(">2B", buf, 0, 86, 90)  # 'VZ'
        struct.pack_into(">I", buf, 4, cmd_len)
        struct.pack_into(">" + str(cmd_len) + "s", buf, 8, cmd_data)

        try:
            tcp_client.sendall(buf)
        except Exception as err:
            print('发送异常{}'.format(traceback.format_exc()))
            raise

    def tcp_send_heartbeat_message_proc(self):
        """
        发送心跳
        :return:
        """
        tcp_client = self.tcp_client
        buf = create_string_buffer(8)
        struct.pack_into(">2B", buf, 0, 86, 90)
        struct.pack_into(">B", buf, 2, 1)  # 0x01
        struct.pack_into(">I", buf, 4, 0)
        tcp_client.sendall(buf)

    def tcp_recv_data_common(self, timeout=10):
        """
        处理接收数据
        break_flag:中断循环标志位
        :return:
        """
        json_res = {}  # 数据处理后的结果
        wait_count = 0  # 收到心跳包次数（防止死循环在心跳包中）
        image_str = ''
        tcp_client = self.tcp_client
        try:
            while True:
                # 设置 recv 超时时间
                ready = select.select([self.tcp_client], [], [], timeout)
                if ready[0]:
                    # 接收结果
                    response = tcp_client.recv(8)
                    if (b'VZ' == response[0:2]):
                        data_len = struct.unpack('>i', bytes(response[4:8]))
                        sleep(1)
                        response = tcp_client.recv(data_len[0])
                        if response == b'':
                            continue

                        # 数据分割定位
                        sear_str_byte = b'}\n'
                        split_index = response.find(sear_str_byte)

                        # 获取非图片部分的json值
                        temp = response[0:split_index + 1]
                        response_str = str(temp, encoding='gbk')
                        # response_str = str(temp,encoding='utf-8')
                        json_res = json.loads(response_str)

                        # 具有图片数据
                        if len(response[split_index:]) > 100:
                            # 获取图片数据
                            image_str = response[split_index + len(sear_str_byte) + 1:]
                        break

                    elif response == b'':  # 心跳包返回空字串
                        wait_count += 1
                        if wait_count <= 1:
                            print('tcp_recv_data 循环等待次数 {}'.format(wait_count))
                            continue
                        else:
                            break
        except Exception as err:
            # print('Fail err is  %s' % (err))
            print('response = {}'.format(response))
        finally:
            # 发送一个心跳
            self.tcp_send_heartbeat_message_proc()
        return json_res, image_str

    def tcp_send_cmd(self, cmd_string_data=''):
        """

        :param cmd_string_data:json结构命令
        :param cmd: tcp协议命令
        :param state_code: 预期状态码
        :param has_image: 0,默认接收数据不包含图片，1代码接收数据包含图片
        :return:
        """
        json_data = {}  # 接受数据
        image_str = ''
        if cmd_string_data == '':
            return json_data
        try:
            # 发送命令
            self.tcp_send_msg_base(cmd_string_data.encode())
            json_data, image_str = self.tcp_recv_data_common()

        except Exception as err:
            print('function {} err is {}  json_data={}'.format(self.__class__.__name__, err, json_data))
            json_data = {}

        return json_data, image_str


class RX_TcpOperation(CommonTcpFuns):
    """
    RX 设备方法合集
    """

    def now_trigger_result(self):
        """
        立即触发
        :return:
        """
        cmd_string_data = '{"cmd":"trigger"}'
        # 发送命令
        self.tcp_send_msg_base(cmd_string_data.encode())
        # self.tcp_client.recv(20480)

    def set_ioctl(self):
        """
        开闸
        :return:
        """
        cmd_string_data = '{"cmd" : "ioctl","id" : "132156","delay" : 500,"io" : 0,"value" : 2}'
        # 发送命令
        self.tcp_send_msg_base(cmd_string_data.encode())
        a =self.tcp_client.recv(10)
        a

    def playserver_voice(self, voice='MTEx'):
        """
        播放语音
        :return:
        """
        cmd_string_data = '{"body" : {"type" : "ps_voice_play","voice" : "%s","voice_interval" : 0,"voice_male" : 1,"voice_volume" : 100},"cmd" : "playserver_json_request","id" : "132156"}' % voice
        # 发送命令
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def send_485_data(self, data='MTIzNDU2Nzg5MA=='):
        """
        发送485数据
        :return:
        """
        # 初始化
        cmd_string_data = '{"cmd" : "ttransmission","data" : "rs485-1","len" : 7,"subcmd" : "init"}'
        # 发送命令
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)
        # 发送485数据
        # cmd_string_data = '{"cmd" : "ttransmission","comm" : "rs485-1","data" : "%s","datalen" : 5,"subcmd" : "send"}' % data
        cmd_string_data = '{"cmd" : "ttransmission","subcmd" : "send","datalen" : 512, "data" :"MDAwMTAyMDMwNDA1MDYwNzA4MDkwQTBCMEMwRDBFMEYxMDExMTIxMzE0MTUxNjE3MTgxOTFBMUIxQzFEMUUxRjIwMjEyMjIzMjQyNTI2MjcyODI5MkEyQjJDMkQyRTJGMzAzMTMyMzMzNDM1MzYzNzM4MzkzQTNCM0MzRDNFM0Y0MDQxNDI0MzQ0NDU0NjQ3NDg0OTRBNEI0QzRENEU0RjUwNTE1MjUzNTQ1NTU2NTc1ODU5NUE1QjVDNUQ1RTVGNjA2MTYyNjM2NDY1NjY2NzY4Njk2QTZCNkM2RDZFNkY3MDcxNzI3Mzc0NzU3Njc3Nzg3OTdBN0I3QzdEN0U3RjgwODE4MjgzODQ4NTg2ODc4ODg5OEE4QjhDOEQ4RThGOTA5MTkyOTM5NDk1OTY5Nzk4OTk5QTlCOUM5RDlFOUZBMEExQTJBM0E0QTVBNkE3QThBOUFBQUJBQ0FEQUVBRkIwQjFCMkIzQjRCNUI2QjdCOEI5QkFCQkJDQkRCRUJGQzBDMUMyQzNDNEM1QzZDN0M4QzlDQUNCQ0NDRENFQ0ZEMEQxRDJEM0Q0RDVENkQ3RDhEOURBREJEQ0REREVERkUwRTFFMkUzRTRFNUU2RTdFOEU5RUFFQkVDRURFRUVGRjBGMUYyRjNGNEY1RjZGN0Y4RjlGQUZCRkNGREZFRkY=", "comm" : "rs485-2"}'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def add_del_white(self):
        """
        增删白名单
        :return:
        """
        pass

    def get_snap_img(self):
        """
        获取截图
        :return:
        """
        cmd_string_data = '{"cmd":"get_snapshot","id":"123456" }'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def test_get_device_bottom_time(self):
        # 获取设备底层时间
        cmd_string_data = '{"cmd":"get_device_timestamp"}'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def test_query_current_offline_status(self):
        cmd_string_data = '{"cmd":"get_offline_status","id":123456,"body":{}}'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def test_configure_data_push_method_002(self):
        # 设置数据推送方式
        cmd_string_data = '{"cmd" : "ivsresult","enable" : true,"format" : "json","image" : true,"image_type" : 2}'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def query_white_list(self):
        """
        查询白名单
        :return:
        """
        cmd_string_data = '{"cmd" : "white_list_operator","id" : "999999","operator_type" : "select","plate" : "川","sub_type" : "plate"}'
        self.tcp_send_msg_base(cmd_string_data.encode())
        self.tcp_client.recv(20480)

    def set_system_time_set_time_forward(self, time_str='2015-03-17 20:47:02'):
        """
        设置系统时间
        :return:
        """
        result_b = True
        try:
            cmd_string_data = '{"cmd":"set_time","timestring":"%s" }' % (time_str)
            data = self.tcp_send_cmd(cmd_string_data)[0]
            print('data = {}'.format(data))


            # 检查信息
            assert data.get('cmd') == 'set_time'
            assert data.get('id') != None
            assert data.get('state_code') == 200
            assert data.get('error_msg') == 'Sucess'
        except Exception as err:
            # print('err is {}'.format(traceback.format_exc()))
            result_b = False
        finally:
            return result_b

    def RX_test_tcp_trigger(self, trigger_num=1, trigger_time=1):
        """
        手动触发识别
        :param trigger_num: 设置触发次数
        :param trigger_time: 设置每次触发间隔时间
        :return: trigger_count 有效触发次数
        """
        try:
            result_b = True
            trigger_count = 0
            # 触发
            for i in range(trigger_num):
                cmd_string_data = '{"cmd":"trigger"}'
                data = self.tcp_send_cmd(cmd_string_data)[0]
                print('data = {}'.format(data))
                # 触发成功计数累加
                if data.get('state_code') == 200:
                    trigger_count += 1
                # 睡眠
                print('有效触发次数= 【{}】'.format(trigger_count))
                sleep(trigger_time)
        except Exception as err:
            result_b = False
            print('err is {}'.format(err))
        finally:
            return result_b

    def add_white_data(self, info_dic):
        """
        添加白名单
        :return:
        """
        # info_dic = {
        #     '车牌号': '钟凯',
        #     '启用': '1',
        #     '开始日期': '2015-12-25 11:00:00',
        #     '过期日期': '2027-12-25 11:00:00',
        #     '开始有效时间段': '00:00:00',
        #     '结束有效时间段': '11:00:00',
        #     '黑名单': '0',
        #     '备注': '没有备注',
        #
        # }
        print('添加或更新白名单')
        cmd_string_data = '{' \
                          '"cmd" : "white_list_operator",' \
                          '"operator_type":"update_or_add",' \
                          '"dldb_rec":{' \
                          '"create_time":"2015-12-25 11:00:00",' \
                          '"enable_time":"%s",' \
                          '"overdue_time":"%s",' \
                          '"enable":%s,  ' \
                          '"plate":"%s",' \
                          '"time_seg_enable":1, ' \
                          '"seg_time_start":"%s",' \
                          '"seg_time_end":"%s",' \
                          ' "need_alarm":%s,' \
                          '"vehicle_code":"1",' \
                          '"vehicle_comment":"%s",' \
                          '"customer_id":144413212}}' % (info_dic['开始日期'], info_dic['过期日期'], info_dic['启用'],
                                                         info_dic['车牌号'], info_dic['开始有效时间段'], info_dic['结束有效时间段'],
                                                         info_dic['黑名单'], info_dic['备注'])

        data = self.tcp_send_cmd(cmd_string_data)[0]
        print('data = {}'.format(data))
        assert data.get('cmd') == 'white_list_operator'
        assert data.get('state_code') == 200

    def set_bit_rate_value(self, serial_port='1', bit='9600', check_bit='0', stop_bit='1', data_bit='8'):
        """
        设置波特率
        :param serial_port: 串口号
        :param bit: 波特率
        :param check_bit: 校验位校验位：
        0．	无校验
        1．	奇校验
        2．	偶校验
        :param stop_bit: 停止位
        :param data_bit: 数据位
        :return:
        """

        cmd_string_data = '{"body" : {"baud_rate" : %s,"data_bits" : %s,"parity" : %s,"stop_bits" : %s},"cmd" : "set_serial_para","id" : "123","serial_port" : 0}' % (
            bit, data_bit, check_bit, stop_bit)
        try:
            result_b = True
            data = self.tcp_send_cmd(cmd_string_data)[0]
            print('data = {}'.format(data))
            # 检查信息
            assert data.get('cmd') == 'set_serial_para'
            assert data.get('state_code') == 200
            assert data.get('error_msg') == 'Sucess'
            # 触发成功计数累加
        except Exception as err:
            result_b = False
            print('err is {}'.format(err))
        finally:
            return result_b


class LogMods():
    # 定义多个日志文件
    def __init__(self, filename=None):
        self.filename = 'log.txt'
        if filename != None:
            self.filename = filename
        # 定义文件
        self.filehandle = logging.FileHandler(filename=self.filename, mode='a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s-%(name)s-%(levelname)s:  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        self.filehandle.setFormatter(fmt)

    def log_err(self, message='', name='', write=True):
        # 定义日志
        log_name = ''
        if name != '':
            log_name = name
        loggerhandle = logging.Logger(name=log_name, level=logging.ERROR)
        loggerhandle.addHandler(self.filehandle)
        # 写日志
        if write != True:
            return
        loggerhandle.error(msg=message)

    def log_info(self, message='', name='', write=True):
        # 定义日志
        log_name = ''
        if name != '':
            log_name = name
        loggerhandle = logging.Logger(name=log_name, level=logging.INFO)
        loggerhandle.addHandler(self.filehandle)
        # 写日志
        if write != True:
            return
        loggerhandle.info(msg=message)

    def log_debug(self, message='', name='', write=True):
        # 定义日志
        log_name = ''
        if name != '':
            log_name = name
        loggerhandle = logging.Logger(name=log_name, level=logging.DEBUG)
        loggerhandle.addHandler(self.filehandle)
        # 写日志
        if write != True:
            return
        loggerhandle.debug(msg=message)


def send_keys(dr, find_way=[], send_value='', outtime=15, check_num=3, clear=True, ):
    """
    重写send_keys，增加健壮性
    :param by: 查找方式
    :param value:
    :param send_value: 填入内容
    :param outtime: 超时时间
    :param check_num: 检查次数
    :return:True、False
    """

    sleep_time_i = int(outtime / check_num)  # 计算 循环检查三次的睡眠时间

    for i in range(check_num):
        # 是否跳出循环标志，默认False跳出
        continue_b = True
        try:
            ele = dr.find_element(find_way[0], find_way[1])
            sleep(0.5)
            # 其清空值
            if clear == True:
                ele.clear()
            # 填入值
            ele.send_keys(send_value)
        except Exception as err:
            sleep(sleep_time_i)
            continue_b = False
        finally:
            # 跳出循环
            if continue_b == True:
                break
    return continue_b


def click(dr, find_way=[], outtime=3, check_num=3):
    """
    重写元素点击，增加健壮性
    :param outtime: 超时时间
    :param check_num: 检查次数
    :return:True、False
    """
    sleep_time_i = int(outtime / check_num)  # 计算 循环检查三次的睡眠时间

    for i in range(check_num):
        # 是否跳出循环标志，默认False跳出
        continue_b = True
        try:
            # 点击跳转
            dr.find_element(find_way[0], find_way[1]).click()
        except Exception as err:
            sleep(sleep_time_i)
            continue_b = False
        finally:
            # 跳出循环
            if continue_b == True:
                break
    return continue_b


def check_ele_is_exist(dr, find_way, outtime=15, check_num=3):
    """
    检查元素是否存在
    :return:
    """
    sleep_time_i = int(outtime / check_num)  # 计算 循环检查三次的睡眠时间

    for i in range(check_num):
        # 是否跳出循环标志，默认False跳出
        continue_b = True
        try:
            # 点击跳转
            dr.find_element(find_way[0], find_way[1])
        except Exception as err:
            sleep(sleep_time_i)
            continue_b = False
        finally:
            # 跳出循环
            if continue_b == True:
                break
    return continue_b


def web_update_dev(ip, upfile, username='admin', password='admin', exit_chorme=True):
    """
    通过网页升级设备
    :return:
    """
    # #先恢复设备正常  reboot
    # linux_telnet = BaseLinuxTelent()
    # linux_telnet.login_host(ip,'root','108balance')
    # linux_telnet.execute_some_command('reboot')
    # print('重启设备中【{}】'.format(ip))
    # print('睡眠240s')
    # sleep(240)

    # 升级设备
    print('初始化登录设备【{}】'.format(ip))
    USERNAME_ELE = [By.ID, 'username']
    PASSWORD_ELE = [By.ID, 'usrpwd']
    LOGIN_BT_ELE = [By.ID, 'submit']

    DEVICE_MAINTENANCE_PAGE = [By.XPATH, './/span[contains(text(),"设备维护")]/parent::a']  # 设备维护
    SYS_MAINTENANCE_PAGE = [By.XPATH, './/span[contains(text(),"系统维护")]/parent::a']  # 【系统维护】
    SOFT_VERSION_ELE = [By.XPATH, './/*[contains(text(),"软件版本")]/following-sibling::td']

    FILE_INPUT_ELE = [By.ID, 'file_input']  # 升级文件
    FILE_UPGRATE_BT_ELE = [By.ID, 'update']  # 升级按钮
    try:
        dr = webdriver.Chrome()
        dr.implicitly_wait(20)
        dr.set_page_load_timeout(15)
        dr.set_script_timeout(15)
        dr.maximize_window()
        dr.get('http://{}/login.htm'.format(ip))
    except Exception as err:
        dev_version_dics_info[ip] = 'web 访问异常无法访问'
        dr.quit()
        raise err

    send_keys(dr, USERNAME_ELE, username)
    sleep(1)
    send_keys(dr, PASSWORD_ELE, password)
    sleep(1)
    click(dr, LOGIN_BT_ELE)
    sleep(1)

    for i in range(5):
        try:
            dr.refresh()
            sleep(5)
            click(dr, DEVICE_MAINTENANCE_PAGE)
            sleep(5)
            print('【{}】跳转到系统维护'.format(ip))
            assert True == click(dr, SYS_MAINTENANCE_PAGE)
        except Exception as err:
            raise err
    sleep(10)

    # 软件版本
    old_version_ele = dr.find_element(SOFT_VERSION_ELE[0], SOFT_VERSION_ELE[1]).text
    sleep(1)
    print('【{}】升级前获取设备版本【{}】'.format(ip, old_version_ele))
    up_bin_name = upfile.split('\\')[-1]
    if up_bin_name.find(old_version_ele) != -1:
        print('【{}】当前已是待升级版本【{}】'.format(ip, up_bin_name))
        dev_version_dics_info[ip] = up_bin_name + '   已是升级版本'
        dr.quit()
        return

    # 选择升级文件
    send_keys(dr, FILE_INPUT_ELE, upfile)
    sleep(2)
    # 点击升级
    click(dr, FILE_UPGRATE_BT_ELE)
    sleep(2)

    if True != check_ele_is_exist(dr, [By.XPATH, './/*[contains(text(),"升级成功")]'], outtime=240, check_num=100):
        if check_ele_is_exist(dr, [By.XPATH, './/*[contains(text(),"重新升级")]'], outtime=120, check_num=100):
            dr.save_screenshot('【{}】升级失败截图'.format(ip))
            print('检查出现【{}】 【重新升级】 字段'.format(ip))
        print('关闭【{}】浏览器'.format(ip))

    print('检查出现【{}】升级成功'.format(ip))
    dr.quit()  # 关闭浏览器
    print('【{}】睡眠240s'.format(ip))
    sleep(240)

    print('重新登录【{}】验证升级是否成功'.format(ip))
    dr = webdriver.Chrome()
    dr.implicitly_wait(20)
    dr.set_page_load_timeout(15)
    dr.set_script_timeout(15)
    dr.maximize_window()
    dr.get('http://{}/login.htm'.format(ip))

    send_keys(dr, USERNAME_ELE, username)
    sleep(1)
    send_keys(dr, PASSWORD_ELE, password)
    sleep(1)
    click(dr, LOGIN_BT_ELE)
    sleep(3)
    # 设备维护
    click(dr, DEVICE_MAINTENANCE_PAGE)
    sleep(5)
    # 系统维护
    click(dr, SYS_MAINTENANCE_PAGE)
    sleep(5)

    # 软件版本
    new_version_ele = dr.find_element(SOFT_VERSION_ELE[0], SOFT_VERSION_ELE[1]).text
    # print('获取设备【{}】升级后版本为【{}】'.format(ip,new_version_ele))
    if up_bin_name.find(new_version_ele) != -1:
        print('设备【{}】升级成功为【{}】'.format(ip, new_version_ele))
        dev_version_dics_info[ip] = new_version_ele + '  升级成功'
    else:
        print('设备【{}】升级失败'.format(ip))
        dev_version_dics_info[ip] = new_version_ele + '  升级失败'

    if exit_chorme == True:
        dr.quit()


def hang_up_device_one(ip, sleep_time=1):
    """
    设备挂机-1
    :return:
    """
    lock = threading.Lock()
    rx_client = RX_TcpOperation(ip, 8131)

    lock.acquire()
    tcp_clients_dic[ip] = rx_client.tcp_client
    lock.release()  # 释放锁

    re_connect_b = False  # 重连
    i = 0
    print('【{}】开始长稳挂机'.format(ip))
    while True:
        try:
            # 异常断开后重连
            if re_connect_b == True:
                rx_client = RX_TcpOperation(ip, 8131)
                re_connect_b = False
                print('长稳:已重新连接【{}】'.format(ip))
                # lock.acquire()
                tcp_clients_dic[ip] = rx_client.tcp_client
                # lock.release()  # 释放锁

            rx_client.now_trigger_result()  # 触发识别
            rx_client.tcp_send_heartbeat_message_proc()  # 发送心跳
            # rx_client.tcp_client.recv(20480)
            # rx_client.get_snap_img()#获取截图
            # rx_client.test_get_device_bottom_time()##获取设备底层时间
            # rx_client.test_configure_data_push_method_002()# # 设置数据推送方式
            # rx_client.test_query_current_offline_status()#获取设备状态
            # rx_client.set_ioctl()  # 控制开闸 延迟很大
            # rx_client.playserver_voice()  # 播放语音
            # rx_client.send_485_data()  # 发送485
            # #获取截图
            # rx_client.query_white_list()  # 查询白名单
            # print('【{}】query whitelist'.format(i))
            sleep(sleep_time)
            i += 1
        except Exception as err:
            re_connect_b = True
            print('err is {}'.format(traceback.format_exc()))
            rx_client.tcp_close_client()


def checkserver(telent, host_ip, server_lists=[]):
    """
    function:检查设备服务进程状态
    :param server_list:服务列表
    :return:not_exist_server 未存在服务
    """
    try:
        not_exist_server = []
        # log.log_info('开始检查{}服务......................................'.format(host_ip),write=False)
        for server in server_lists:
            # 检查当前服务是否存在
            cmd = 'ps -A|grep {}|grep -v "grep {}"'.format(server, server)
            # log.log_info('执行命令: {}'.format(cmd),write=False)
            # 执行命令
            response_str = telent.excute_some_command_until(cmd, "~ #")
            # log.log_info('返回结果:{}'.format(response_str),write=False)
            now_time = datetime.datetime.now()
            kill_now_time = now_time.strftime('%Y_%m_%d %H_%M_%S')
            if response_str.find(server) == -1:
                #查看当前内存
                print('{}的服务{} 未发现'.format(host_ip, server))
                if record_raise_err_time[host_ip][server]['server_status'] == None or \
                                record_raise_err_time[host_ip][server]['server_status'] == True:
                    # 获取服务开始运行时间
                    server_run_time = record_raise_err_time[host_ip][server]['server_start_time']
                    # 计算时间差
                    total_seconds = (now_time - server_run_time).seconds
                    hours = '%.2f' % (total_seconds / 3600.0)

                    record_raise_err_time[host_ip][server]['restore_num'].append(
                            '服务【{}】运行【{}小时】 开始运行时间【{}】 挂掉时间【{}】'.format(
                                    server, hours, server_run_time.strftime('%Y-%m-%d %H:%M:%S'),
                                    now_time.strftime('%Y-%m-%d %H:%M:%S')))

                    record_raise_err_time[host_ip][server]['server_status'] = False  # 相应服务挂死标志位
                not_exist_server.append(server)

            # 服务恢复时间
            else:
                # 挂机恢复标志位

                if record_raise_err_time[host_ip][server]['server_status'] == False:
                    # 重置服务开始运行时间
                    record_raise_err_time[host_ip][server]['server_start_time'] = datetime.datetime.now()
                    record_raise_err_time[host_ip][server]['server_status'] = True  # 由挂死恢复运行重置标志位
                elif record_raise_err_time[host_ip][server]['server_status'] == True:
                    # 模块已重启后未再挂死
                    record_raise_err_time[host_ip][server]['server_status'] = None  # 服务为运行状态


    except:
        # log.log_err('查询【{}】服务失败 err is {}'.format(host_ip,traceback.format_exc()),write=False)
        pass
    finally:
        telent.logout_host()
        # 存在服务挂掉返回False
        if len(not_exist_server):
            return False, not_exist_server
        # log.log_info('{}所有服务启用成功'.format(host_ip),write=False)
        return True, []


def mass_reboot_dev(ip_list=[], server_lists=[], check_num=4, username='root', password='108balance', log=None):
    """
    批量重启设备
    :param ip_list:
    :param server_lists:
    :return:
    """
    threading_update_list = []  # 重启设备线程
    for ip in ip_list:
        t = threading.Thread(target=reboot_dev, args=(ip, server_lists, check_num, username, password, log,))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_update_list.append(t)
        print('########设备【{}】重启中#########'.format(ip))
        t.start()

    for thread_t in threading_update_list:
        thread_t.join()  # 设置主线程等待子线程结束


def reboot_dev(ip, server_lists=[], check_num=4, username='root', password='108balance', log=None):
    """
    重启设备并检查服务状态
    :param ip:
    :param server_lists: 服务列表
    :param check_num: 检查次数  每次默认60s间隔
    :param username:
    :param password:
    :param log: 日志对象
    :return:
    """

    # 先恢复设备正常  reboot
    linux_telnet = BaseLinuxTelent()
    try_connect_b = False
    try:
        # 设置失败尝试次数
        for i in range(3):
            if try_connect_b == True:
                linux_telnet = BaseLinuxTelent()
            # 如果登录结果返加True，则执行命令，然后退出
            if linux_telnet.login_host(ip, username, password):
                linux_telnet.execute_some_command('reboot')  # 执行命令
            break
            sleep(10)
    except Exception as err:
        try_connect_b == True
        linux_telnet.logout_host()

    # 循环检查重启是否成功
    reboot_success_b = False
    try:
        for i in range(check_num):
            sleep(60)  # 60s检查
            if linux_telnet.login_host(ip, username, password):
                reboot_success_b = True
                print('重启设备:【{}】【{}】重启成功'.format(i, ip))
                log.log_info('重启设备:【{}】【{}】重启成功'.format(i, ip))
                break
            print('重启设备:【{}】【{}】还未启动，等待60s后再次检查'.format(i, ip))

    except Exception as err:
        pass
    finally:
        if reboot_success_b == False:
            print('重启设备:【{}】重启失败'.format(ip))
            log.log_info('重启设备:【{}】重启失败'.format(ip))
            dev_reboot_err_dic[ip] = '重启异常未恢连接'
            raise err

    server_ok_b = False
    no_exist_server_list = []
    for i in range(check_num):
        sleep(60)
        # 检查服务是否允许起来
        ret_b, server_list = checkserver(linux_telnet, ip, server_lists)
        if ret_b == True:
            print('重启设备:【{}】 【{}】 服务启用成功'.format(i, ip))
            log.log_info('重启设备:【{}】 【{}】 服务启用成功'.format(i, ip))
            server_ok_b = True
            no_exist_server_list = []
            break
        else:
            log.log_err('重启设备:【{}】未检查到【{}】服务'.format(ip, server_list))
            no_exist_server_list = server_list
        print('重启设备;【{}】次检查服务'.format(ip))

    if server_ok_b == False:
        dev_reboot_err_dic[ip] = '重启设备:服务未启用成功【{}】'.format(no_exist_server_list)


def testcheckserverstate(ip_list=[], server_lists=[], sleep_time=300, log=None):
    """
    监控设备服务是否存在
    :return:
    """

    while True:
        ip_err_dic = {}
        for ip in ip_list:
            try:
                linux_telnet = BaseLinuxTelent()
                # 如果登录结果返加True，则执行命令，然后退出
                if not linux_telnet.login_host(ip, 'root', '108balance'):
                    print('【{}】设备无法登录'.format(ip))
                    ip_err_dic[ip] = '设备无法登录'
                    continue
                # log.log_info('登录设备{dev_ip}成功',write=False)

                ret_b, server_list = checkserver(linux_telnet, ip, server_lists)

                for server_name in server_lists:
                    # 记录服务重启次数
                    if len(record_raise_err_time[ip][server_name]['restore_num']) != 0:
                        des_str = '目前【{}】的【{}】已挂死【{}】次'.format(ip, server_name, len(
                                record_raise_err_time[ip][server_name]['restore_num']))
                        print(des_str)
                        log.log_err(des_str)
                        des_str = '{}服务异常记录列表 restore_num ={}'.format(server_name,
                                                                      record_raise_err_time[ip][server_name][
                                                                          'restore_num'])
                        print(des_str)
                        log.log_err(des_str)

                # 服务有异常
                if ret_b == False:
                    ip_err_dic[ip] = str(server_list)
                else:
                    print('{} 服务启用成功'.format(ip))
                    log.log_info('{} 服务启用成功'.format(ip))

            except Exception as err:
                # print('查询{} 服务状态失败 err is {}'.format(ip, traceback.format_exc()))
                log.log_err('查询{} 服务状态失败 err is {}'.format(ip, traceback.format_exc()))
                ip_err_dic[ip] = '查询服务失败 失败原因【{}】'.format(traceback.format_exc())

        # 有异常服务
        if len(ip_err_dic) != 0:
            send_str = ''
            for key, value in ip_err_dic.items():
                des_str = '\n******************************\n 【{}】设备挂掉服务{} \n ******************************'.format(
                    str(key), value)

                if value == '查询服务失败':
                    des_str = '【{}】设备登录失败 【】'.format(str(key, value))

                print(des_str)
                log.log_err(des_str)
                send_str += des_str + '\n'
                send_email_qq_one(des_str,subject='【{}】后台服务检查'.format(ip))

        for ip in ip_list:
            if ip_err_dic.get(ip) == None:
                log.log_info(
                    '\n******************************\n【{}】设备所有服务正常\n******************************'.format(ip))
                print('\n******************************\n【{}】设备所有服务正常\n******************************'.format(ip))

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('检查完成时间 【{}】 睡眠{}s'.format(nowTime, sleep_time))
        log.log_info('检查完成时间 【{}】 睡眠{}s'.format(nowTime, sleep_time))
        print('################################################################################')
        log.log_info("####################################################################################")
        sleep(sleep_time)


def mass_tcp_recv_data(ip_list):
    """
    批量接收数据
    :return:
    """
    sleep(3)
    threading_tcp_recv_list = []  # 接收数据线程
    for ip in ip_list:
        t = threading.Thread(target=tcp_recv_data_common, args=(ip, 1,))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_tcp_recv_list.append(t)
        t.start()
        print('########设备【{}】已开始监听接收数据#########'.format(ip))

    for thread_t in threading_tcp_recv_list:
        thread_t.join()  # 设置主线程等待子线程结束


def mass_upgrade(ip_list=[], upfile_file='', log=None, exit_chorme=True):
    """
    批量升级设备
    :param ip_list: 设备列表
    :param upfile_file: 升级文件
    :param log: 日志对象
    :return:
    """

    # 升级设备
    threading_update_list = []  # 升级线程
    for ip in ip_list:
        t = threading.Thread(target=web_update_dev, args=(ip, upfile_file, 'admin', 'admin', exit_chorme))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_update_list.append(t)
        t.start()
        sleep(120)
        print('########设备【{}】已开始升级#########'.format(ip))

    for thread_t in threading_update_list:
        thread_t.join()  # 设置主线程等待子线程结束

    print(dev_version_dics_info)
    log.log_info("总计{}台升级结果:【{}】".format(len(dev_version_dics_info), dev_version_dics_info))


def run_hang_up_script(ip_list):
    # 更新挂机时间
    nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file_name = os.path.join(os.path.dirname(__file__), '【{}】8.2.1.2020090150 全量跑更新为1s触发.txt'.format(nowTime))
    # file_name = os.path.join(os.path.dirname(__file__), '【{}】RM 挂机1s触发.txt'.format(nowTime))
    log = LogMods(filename=file_name)

    # 服务进程列
    server_lists = [
        'log_server',  # 日志
        'dp_server',
        'system_server_app',
        'media_server',
        'alg_server_app',  # 算法
        'record_server_app',
        'extern_device_app',
        'xtp_push_app',  # http/ftp推送
        'bus_server_app',  # 网页
        'batch_server_app',
        'devgrp_server_app',
        'web_run_rx',  # 外设
        'tcp_rx_app',
        'onvif_server_app',  # 批量操作
        'stp_server_app',  # 上云'
        'vsftpd',
    ]

    server_lists = [
         'app_entry_linux']

    # 先恢复设备正常  reboot
    #mass_reboot_dev(ip_list, server_lists, log=log)

    # 异常设备取消后续挂机操作，从挂机列表中删除
    # if len(dev_reboot_err_dic) != 0:
    # log.log_info("设备重启：设备异常结果:【{}】".format(dev_reboot_err_dic))
    # print("设备重启：设备异常结果:【{}】".format(dev_reboot_err_dic))
    # for ip in dev_reboot_err_dic.keys():
    #     ip_list.remove(ip)
    #     log.log_err('移除异常设备【{}】'.format(ip))

    # 升级文件
    # bin_name = 'VZ_RX_8.2.1.202005170_u19k17r38a314.bin'
    # upfile_file = os.path.join(os.getcwd(), bin_name)
    # print('升级镜像文件【{}】'.format(bin_name))
    # mass_upgrade(ip_list=ip_list,upfile_file=upfile_file,log=log)
    # mass_upgrade(ip_list=ip_list,upfile_file=upfile_file,log=log,exit_chorme=False) #升级完成后不关闭浏览器

    # 记录服务开始运行时间
    for ip in ip_list:
        record_raise_err_time[ip] ={}
        for server_name in server_lists:
            record_raise_err_time[ip][server_name] ={}
            #服务运行开始时间
            record_raise_err_time[ip][server_name]['server_start_time'] =  datetime.datetime.now()
            # 服务运行状态标志位
            record_raise_err_time[ip][server_name]['server_status'] =  None
            #异常记录
            record_raise_err_time[ip][server_name]['restore_num'] = []

    threading_hang_up_list = []  # 挂机线程

    # 检查设备状态
    t = threading.Thread(target=testcheckserverstate, args=(ip_list, server_lists, 60, log,))
    t.setDaemon(True)
    threading_hang_up_list.append(t)
    print('长稳:开始检查所有设备服务状态')
    t.start()

    # 挂机
    for ip in ip_list:
        t = threading.Thread(target=hang_up_device_one, args=(ip, 1))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_hang_up_list.append(t)
        t.start()

    #接收数据，不做处理
    mass_tcp_recv_data(ip_list=ip_list)

    for thread_t in threading_hang_up_list:
        thread_t.join()  # 设置主线程等待子线程结束
    print("end")


def anay_log_dic(data={}):
    """

    :param data:
    :return:
    """
    log_data_dic = data['body']


def mass_tcp_send_mass(ip_list):
    # 升级设备
    threading_update_list = []  # 升级线程
    for ip in ip_list:
        t = threading.Thread(target=hang_up_device_one, args=(ip,))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_update_list.append(t)
        t.start()
        sleep(5)
        print('########设备【{}】已开始挂机tcp#########'.format(ip))

    for thread_t in threading_update_list:
        thread_t.join()  # 设置主线程等待子线程结束


def mass_tcp_send_cmd(ip_list):
    # 升级设备
    mass_tcp_send_mass(ip_list)
    # mass_tcp_recv_data(ip_list)


def check_free(ip,username='root',password='108balance',sleep_time=5):
    nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file_name = os.path.join(os.path.dirname(__file__), '【{}】【{}】内存记录.txt'.format(nowTime,ip))
    free_log = LogMods(filename=file_name)

    telent = BaseLinuxTelent()
    check_flag = False
    for i in range(3):
        if telent.login_host(ip,username,password) == False:
            free_log.log_err('【{}次】telnet 登录失败'.format(i))
            sleep(60)
            continue
        check_flag = True
        break
    while check_flag == True:
        cmd = 'free -m'
        res_content = telent.excute_some_command_until(cmd,'~ #')
        if res_content == None:
            telent.login_host(ip,username,password)
        print(res_content)
        free_log.log_info(res_content)
        sleep(sleep_time)


def mass_check_free(ip_list):
    # 升级设备
    threading_update_list = []  # 升级线程
    for ip in ip_list:
        t = threading.Thread(target=check_free, args=(ip,))
        t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
        threading_update_list.append(t)
        t.start()
        sleep(5)
        print('########设备【{}】已开始挂机间隔5s查看内存#########'.format(ip))

    for thread_t in threading_update_list:
        thread_t.join()  # 设置主线程等待子线程结束

if __name__ == '__main__':
    ip_list = [
   '192.168.112.96',
   '192.168.112.98',
   '192.168.112.105',
   '192.168.112.108',
   '192.168.112.113',
   '192.168.112.126',
   '192.168.112.206',
    ]


    ip_list = [
         '192.168.113.115',
         '192.168.113.18',
        '192.168.113.110',
        '192.168.113.111',
     ]
   #触发挂机
    # run_hang_up_script(ip_list)
    #内存查看
    # mass_check_free(ip_list)
