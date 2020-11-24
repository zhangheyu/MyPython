import socket
import datetime
from multiprocessing import Process


class webServer:
    def init(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 80))
        self.server_socket.listen(100)
        self.cnt = 0

    def start(self):
        print("cnt = %d" % self.cnt)
        client_socket, client_address = self.server_socket.accept()
        self.cnt += 1
        print("connected from[%s, %s]" % client_address)
        start_client_process = Process(target=self.client_server, args=(client_socket, client_address))
        start_client_process.start()
        client_socket.close()

    def client_server(self, client_socket, client_addr):
        request_data = client_socket.recv(1024)
        # 打印日志
        self.log(request_data)
        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
        if request_data.decode().find("zbz") > 0:
            print('张柏芝')
            filename = "zbz.jpg"
            with open(filename, 'rb+') as f:
                body = f.read()
                f.close()
            client_socket.send(body)
        else:
            print('阿娇')
            filename = "index.html"
            with open(filename, encoding='utf-8') as f:
                body = f.read()
                f.close()
                # print(body)
            response = response_start_line + response_headers + "\r\n" + body
            client_socket.send(bytes(response, "utf-8"))
        client_socket.close()

    def main(self):
        self.init()
        while True:
            self.start()

    def log(self, data):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("log.txt", 'a+') as f:
            f.write("\n%s\n%s" % (now_time, data))


if __name__ == '__main__':
    res = webServer()
    res.main()
