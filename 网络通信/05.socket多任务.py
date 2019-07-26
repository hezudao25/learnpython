import socket
import threading

def send_msg(udp_socket,dest_ip,dest_port):
    """接受数据并显示"""
    while True:
        send_data = input("请输入内容:")
        udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))
        if send_data == "exit":
            break

def recv_msg(udp_socket):
    """发送数据"""
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print("来自：%s : %s" % (recv_data[1], recv_data[0].decode("gbk")))

def main():
    """完成udp聊天器的群体控制"""
    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 绑定本地信息
    udp_socket.bind(("", 8081))
    # 3 .获取对方的IP
    dest_ip = input("请输入对方IP：")
    dest_port = int(input("请输入对方的端口："))
    # 4 创建2个线程
    t1 = threading.Thread(target=send_msg, args=(udp_socket, dest_ip, dest_port))
    t2 = threading.Thread(target=recv_msg, args=(udp_socket,))


    # 提交线程
    t1.start()
    t2.start()


    #udp_socket.close()

if __name__ == "__main__":
    main()
