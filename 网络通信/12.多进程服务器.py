import socket
import re
import multiprocessing
def service_client(new_socket):

    """为这个客户端返回数据"""
    # 1. 接收浏览器发来的请求，即http请求
    request = new_socket.recv(1024).decode("utf-8")
    request_list = request.splitlines()
    #print(request_list)
    ret = re.match(r"[^/]+(/[^ ]*)", request_list[0])
    if ret:
        print(ret.group(1))
    else:
        print("正则表达式有问题")

    # 解码

    # 2 返回HTTP格式

    response = "HTTP/1.1 200 OK\r\n"
    response += "\r\n"

    response +="<h1>haha</h1>"
    new_socket.send(response.encode("utf-8"))

    new_socket.close()





def main():
    """"""
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置当服务器先close 即服务器4次挥手之后资源能够立即释放，这样保证
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp_server.bind(("", 7788))

    tcp_server.listen(128)

    while True:

        new_socket, client_addr = tcp_server.accept()
        print('Connected by', client_addr)
        p = multiprocessing.Process(target=service_client, args=(new_socket,))
        p.start()
        new_socket.close()

        #service_client(new_socket)

    tcp_server.close()


if __name__ == '__main__':
    main()