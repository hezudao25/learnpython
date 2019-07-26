#!/usr/bin/env python3
import time
import socket


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
                recv_data = socket_item.recv(1024)  
            except Exception as ret:
                #print(ret)
                print("没有传数据")
            else:
                if recv_data:
                    print(recv_data.decode("utf-8"))
                else:
                    print("客户端关闭")
                    socket_item.close()
                    client_socket_list.remove(socket_item)



if __name__ == "__main__":
    main()



