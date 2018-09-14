import socket

tcp_server_socket=socket.socket (socket.AF_INET,socket.SOCK_STREAM)
tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# 绑定
tcp_server_socket.bind(('',7890))
# 监听套接字
tcp_server_socket.listen(123)
# accept 会造成堵塞
tcp_server_socket.setblocking(False)
client_socket_list =list()

while True:
    try:
        #创建监听套接字
        client_socket,client_addr=tcp_server_socket.accept()

    except Exception as ret:
        print('没有接收到客户')
    else:
        print('接收到客户')
        client_socket.setblocking(False)
        client_socket_list.append(client_socket)
        for client_server in client_socket_list:
            try:
                recv_client =tcp_server_socket.recv(1024)
            except Exception as ret:
                print(ret)
                print('没有接收到客户')
            else:
                if recv_client:
                    print('有消息'）
                else:
                    client_socket_list.remove(client_socket)
                    client_server.close()
                    print('没有收到消息')
                

