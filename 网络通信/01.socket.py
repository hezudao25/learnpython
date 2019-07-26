import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    send_data = input("请输入内容:")
    s.sendto(send_data.encode("utf-8"),("192.168.33.53",80))
    s.close()


if __name__ == "__main__":
    main()
