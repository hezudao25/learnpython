#!/usr/bin/env python3

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    # 由于监听 socket 被注册到了 selectors.EVENT_READ 上，它现在就能被读取，
    # 我们调用 sock.accept() 后立即再立即调 conn.setblocking(False) 来让 socket 进入非阻塞模式
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    # 接着我们使用了 types.SimpleNamespace 类创建了一个对象用来保存我们想要的 socket 和数据，
    # 由于我们得知道客户端连接什么时候可以写入或者读取，下面两个事件都会被用到：
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # 事件掩码、socket 和数据对象都会被传入 sel.register()
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    # 这就是多连接服务端的核心部分，key 就是从调用 select() 方法返回的一个具名元组，
    # 它包含了 socket 对象「fileobj」和数据对象。mask 包含了就绪的事件
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # 如果 socket 就绪而且可以被读取，mask & selectors.EVENT_READ 就为真，
        # sock.recv() 会被调用。所有读取到的数据都会被追加到 data.outb 里面。随后被发送出去
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            # 这表示客户端关闭了它的 socket 连接，这时服务端也应该关闭自己的连接。
            # 不过别忘了先调用 sel.unregister() 来撤销 select() 的监控
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # 当 socket 就绪而且可以被读取的时候，对于正常的 socket 应该一直是这种状态，
            # 任何接收并被 data.outb 存储的数据都将使用 sock.send() 方法打印出来。
            # 发送出去的字节随后就会被从缓冲中删除
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:   # 需要传入参数 :python multiconn-server.py 127.0.0.1 54321
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
# 配置 socket 为非阻塞模式，这个 socket 的调用将不在是阻塞的。
# 当它和 sel.select() 一起使用的时候（下面会提到），我们就可以等待 socket 就绪事件，
# 然后执行读写操作
lsock.setblocking(False)
# sel.register() 使用 sel.select() 为你感兴趣的事件注册 socket 监控，
# 对于监听 socket，我们希望使用 selectors.EVENT_READ 读取到事件
# data 用来存储任何你 socket 中想存的数据，当 select() 返回的时候它也会返回。
# 我们将使用 data 来跟踪 socket 上发送或者接收的东西
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        """sel.select(timeout=None) 调用会阻塞直到 socket I/O 就绪。它返回一个(key, events) 元组，
        每个 socket 一个。key 就是一个包含 fileobj 属性的具名元组。key.fileobj 是一个 socket 对象，
        mask 表示一个操作就绪的事件掩码 """
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # 如果 key.data 为空，我们就可以知道它来自于监听 socket，
                # 我们需要调用 accept() 方法来授受连接请求。我们将使用一个 accept() 包装函数来获取新的
                # socket 对象并注册到 selector 上，我们马上就会看到
                accept_wrapper(key.fileobj)
            else:
                #如果 key.data 不为空，我们就可以知道它是一个被接受的客户端 socket，
                # 我们需要为它服务，接着 service_connection() 会传入 key 和 mask
                #参数并调用，这包含了所有我们需要在 socket 上操作的东西
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()