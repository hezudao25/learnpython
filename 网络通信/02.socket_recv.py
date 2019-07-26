#coding=utf-8

import socket

def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind(('',7788))
    revc_data = udp_socket.recvfrom(1024)
    print(revc_data)
    udp_socket.close()

if __name__ == "__main__":
    main()