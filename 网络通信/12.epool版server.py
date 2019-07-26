from socket import *
import select


def tcp_server(new_tcp_socket, request):

    request_lines = request.splitlines()
    print(request_lines)
    print(">" * 30)
    try:
        file = open("./test/login.html", "rb")
    except:
    	# 构造响应头
        response_header = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header += "\r\n"
        response_header += "----file not found-----"
        new_tcp_socket.send(response_header.encode("utf-8"))
    else:
        html_content = file.read()
        file.close()
        response_body = html_content
        response_header = "HTTP/1.1 200 OK\r\n"
        # 使用Content-Length实现长连接
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"
        response = response_header.encode("utf-8") + response_body
        # 发送响应数据
        new_tcp_socket.send(response)


def main():
    """对大致流程进行控制"""
    # 1.创建tcp套接字
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    # 设置当服务器先close()即服务器4次挥手之后资源立即释放
    tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 2.绑定端口
    tcp_socket.bind(("", 7890))
    # 3.监听套接字
    tcp_socket.listen(128)
    tcp_socket.setblocking(False)
    # 创建一个epoll对象
    epl = select.epoll()
    # 将监听套接字对应的fd注册到epoll中，并绑定事件   fd:文件描述符
    epl.register(tcp_socket.fileno(), select.EPOLLIN)
    # 定义保存socket的字典
    fd_event_dict = dict()
    while True:
        # 默认堵塞，直到OS检测到数据到来过通事件通知方式告诉程序，才会解堵塞 返回list
        fd_event_list = epl.poll()
        # [(fd,event)] (套接字对应的文件描述符，这个文件描述符对应的到底是什么事件，例如可以调用recv接收等)

        # 遍历元组
        for fd, event in fd_event_list:
            if fd == tcp_socket.fileno():
                new_tcp_socket, client_addr = tcp_socket.accept()
                epl.register(new_tcp_socket.fileno(), select.EPOLLIN)
                # 通过字典保存socket，键为fd,值为socket
                fd_event_dict[new_tcp_socket.fileno()] = new_tcp_socket
            elif event == select.EPOLLIN:
                # 判断已经链接的客户端是否有数据发送过来
                recv_data = fd_event_dict[fd].recv(1024).decode("utf-8")
                if recv_data:
                    # 有数据操作
                    # 4.为这个客户端服务
                    tcp_server(fd_event_dict[fd], recv_data)
                else:
                    # 无数据操作
                    fd_event_dict[fd].close()
                    epl.unregister(fd)
                    del fd_event_dict[fd]
    # 关闭监听套接字
    tcp_socket.close()


if __name__ == '__main__':
    main()

