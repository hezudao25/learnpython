#!/usr/bin/env python3
import time
import socket
import re

def service_client(new_socket, request):

    """为这个客户端返回数据"""
    # 1. 接收浏览器发来的请求，即http请求
    #request = new_socket.recv(1024).decode("utf-8")
    request_list = request.splitlines()
    #print(request_list)
    ret = re.match(r"[^/]+(/[^ ]*)", request_list[0])

    if ret:
        if ret.group(1) == "/":
            msg = "/index.html"
        else:
            msg = ret.group(1)
    else:
        msg = "正则表达式有问题"

    # 解码

    # 2 返回HTTP格式
    response_body = "<h1>%s</h1>" % msg

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Length:%d\r\n" % len(response_body)
    response += "\r\n"

    response += response_body
    new_socket.send(response.encode("utf-8"))

    new_socket.close()



def main():
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcp_server.bind(("",7788))
    tcp_server.listen(124)
    tcp_server.setblocking(False)

    client_socket_list = []

    while True:
        time.sleep(0.5)
        try:
            new_socket, new_addr = tcp_server.accept()
        except Exception as ret:
            print("没有新的客户端")
        else:
            print("---")
            tcp_server.setblocking(False)
            client_socket_list.append(new_socket)

        for socket_item in client_socket_list:
            try:
                recv_data = socket_item.recv(1024).decode("utf-8")
            except Exception as ret:
                #print(ret)
                print("没有传数据")
            else:
                if recv_data:
                    service_client(socket_item, recv_data)
                else:
                    socket_item.close()
                    client_socket_list.remove(socket_item)



if __name__ == "__main__":
    main()



