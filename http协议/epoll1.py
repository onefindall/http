import re
import socket
import select

def server(new_socket,request):

    request_lines =request.splitlines()
    # print(request_lines)

    ret = re.match(r'[^/]+(/[^ ]*)',request_lines[0])
   

    file_name =ret.group(1)
    print(file_name)

    if file_name  =='/':
        file_name ='/index.html'
    try:
        f=open('./html'+file_name,'rb')
    except Exception as ret:
        response_body = 'NOT FOUND'
        response = 'HTTP/1.1 404 Not found \r\n'
        response +='Content-Length:%d \r\n'%len(response_body)
        response +='\r\n'
        response +=response_body 
        
        new_socket.send(response.encode('utf-8'))
    else:
        response_body = f.read()
        f.close()
        response_header = 'HTTP/1.1 200 OK \r\n'
        response_header +='Content-Length:%d \r\n'%len(response_body)
        response_header += '\r\n'
        response =response_header.encode('utf-8')+response_body
        new_socket.send(response)



def main():
    tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind(('',7895))
    tcp_server_socket.listen(128)
    # 解堵塞
    tcp_server_socket.setblocking(False)
    # 创建对象
    epl=select.epoll()

    # 将监听套接字对应的fd放到epoll中
    epl.register(tcp_server_socket.fileno(), select.EPOLLIN)
    
    fd_event_dict =dict()

    while True:
        # 检测数据
        fd_event_list =epl.poll()
        for fd,event in fd_event_list:

            if fd == tcp_server_socket.fileno():

                new_socket,client_addr =tcp_server_socket.accept()
                epl.register(new_socket.fileno(),select.EPOLLIN)
		# 把fd放到字典里面
                fd_event_dict[new_socket.fileno()]=new_socket
            else :
                # 接收消息
                recv_data =fd_event_dict[fd].recv(1024).decode('utf-8')
		
                if recv_data:
		# 传参
                    server(fd_event_dict[fd],recv_data)

                else:
                    fd_event_dict[fd].close()

                    epl.unregister(fd)
                    del fd_event_dict[fd]

if __name__ =='__main__':
    main()
