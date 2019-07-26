import socket
import multiprocessing
import re
import sys

class Wsgi_service(object):
    """实现WSGI服务器"""
    def __init__(self, port, app, static_path):
        # 套接字
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close 即服务器4次挥手之后资源能够立即释放，这样保证
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.tcp_server.bind(("", port))

        self.tcp_server.listen(128)
        self.application = app
        self.static_path = static_path


    def service_client(self, new_socket):
        """"""
        requests = new_socket.recv(1024).decode("utf-8")
        requestlines = requests.splitlines()
        if len(requestlines)>0:
            ret = re.match(r"[^/]+(/[^ ]*)", requestlines[0])
            if ret:
                file_name = ret.group(1)
                if file_name == "/":
                    file_name = "/index.html"
            else:
                print("路径有错误")
                return

            if not file_name.endswith(".html"):
                try:
                    f = open(self.static_path + file_name, "rb")
                except:
                    response = "HTTP/1.1 404 Not Found\r\n"
                    response += "\r\n"

                    response += "<h1>file not found</h1>"
                    new_socket.send(response.encode("utf-8"))
                else:
                    html_content = f.read()

                    response = "HTTP/1.1 200 OK\r\n"
                    response += "Content_Lenght:" + str(len(html_content)) + "\r\n"
                    response += "\r\n"

                    new_socket.send(response.encode("utf-8"))
                    new_socket.send(html_content)
                    f.close()
            else:
                environ = dict()
                environ["PATH_INFO"] = file_name
                body = self.application(environ, self.response_code)
                # 则是动态文集
                header = "HTTP/1.1 %s\r\n" % self.status
                for tem in self.headers:
                    header += "%s:%s\r\n" % (tem[0], tem[1])
                header += "\r\n"

                new_socket.send(header.encode("utf-8"))
                new_socket.send(body)

        new_socket.close()


    def response_code(self, status, headers):
        self.status = status
        self.headers = headers
        self.headers += [("Service", "mini web")]


    def run(self):
        """"""
        while True:
            # 1 创建接受接口
            new_socket, new_addr = self.tcp_server.accept()

            # 2 多进程
            mult = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            mult.start()
            new_socket.close()


        self.tcp_server.close()






def main():
    """控制整体，创建一个WEB服务器对象，然后调用这个对象的RUN——FOREVER方法"""
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
        except:
            print("port is error")
            return
    else:
        print("python3 web_server.py 7890 mini_frame:application")
        return

    ret = re.match(r"(^.+):(.*)", sys.argv[2])
    if ret:
        mkname = ret.group(1)
        ffname = ret.group(2)
    else:
        print("python3 web_server.py 7890 mini_frame:application")
        return

    with open("./web_server.conf", "r") as f:
        conf = eval(f.read())

    sys.path.append("./dynamic")
    appname = __import__(mkname)
    app = getattr(appname, ffname)

    wsgl_server = Wsgi_service(port, app, conf["static_path"])
    wsgl_server.run()


if __name__ == '__main__':
    main()