import re
import socket
import select

def server(new_socket,response):
    response_line=response.splitlines()
    ret =re.match(r'[^/]+(/[^ ]*)',response_line[0])
    file_name =ret.group(1)
    print(file_name)
    if file_name =='/':
        file_name ='/index.html'
    try:
        f= open('./html'+file_name,'rb')
    except Exception as ret:
        response_content = 'Not Found'
        response = 'HTTP/1.1 404 NOT FOUND \r\n'
        
        response += 'Content-Length:%d \r\n'%len(response_content)
        response += '\r\n'
        response += response_content
        new_socket.send(response.encode('utf-8'))
    else:
        response_body =f.read()
        f.close()
        response_header = 'HTTP/1.1 200 OK \r\n'
        response_header += 'Content-Length:%d \r\n'%len(response_body)
        response_header += '\r\n'
        response =response_header.encode('utf-8')+response_body
        new_socket.send(response)


def main():
    tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind(('',7888))
    tcp_server_socket.listen(128)
    tcp_server_socket.setblocking(False)
    
    eql=select.epoll()
    eql.register(tcp_server_socket.fileno(),select.EPOLLIN)
    fd_event_dict=dict()
    
    while True:
        eql_event_list =eql.poll()
        for fd,event in eql_event_list:
            if fd == tcp_server_socket.fileno():
                new_socket,clinet_addr =tcp_server_socket.accept()
                eql.register(new_socket.fileno(),select.EPOLLIN)
                fd_event_dict[new_socket.fileno()]=new_socket
            else:
                recv_data= fd_event_dict[fd].recv(1024).decode('utf-8')

                if recv_data:
                    server(fd_event_dict[fd],recv_data)
                else:
                    fd_event_dict[fd].close()
                    eql.unregister(fd)
                    del fd_event_dict[fd]


if __name__ == '__main__':
    main()
