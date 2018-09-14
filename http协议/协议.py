import socket
import re
def server(new_client):
    recv_data= new_client.recv(1024).decode('utf-8')
    # print(recv_data)
    # 列表
    recv_line = recv_data.splitlines()
    print('-'*50)
    print(recv_line)
    file_name= ''
    ret= re.match(r'[^/]+(/[^ ]*)',recv_line[0])
    if ret:
        file_name= ret.group(1)
        if file_name =='/':
            file_name ='/index.html'
    try:
        f= open('./html'+ file_name,'rb')
    except:
        response = 'HTTP/1.1 404 NOT Found\r\n'
        response += '\r\n'
        response += '-----file not found-------'
        new_client.send(response.encode('utf-8'))
    else:
        html_content = f.read()
        f.close()

        response= 'HTTP/1.1 200 OK \r\n'
        response += '\r\n'
    # response += 'jjjjlin'
        new_client.send(response.encode('utf-8'))
        new_client.send(html_content)

    new_client.close()



def main():

    # 创建套接字
    tcp_socket_server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    # 绑定
    tcp_socket_server.bind(('',7885))
    # 换被动为主动
    tcp_socket_server.listen(128)
    while True:
        new_client,client_addr=tcp_socket_server.accept()
        server(new_client)
    tcp_socket_server.close()
if __name__ == '__main__':
    main()
