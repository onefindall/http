#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-26 19:38:28
# @Author  : itcast (python@itcast.cn)
# @Link    : http://www.itcast.cn/subject/pythonzly/index.shtml
# @Version : $Id$
import socket
import re
import multiprocessing

def server(new_client):
	# 接收消息
	recv_data =new_client.recv(1024).decode('utf-8')
	# 客户端也有可能先关闭的话，返回回来的可能是一个空字符，下面要用分割的话有可能报错
	content_split =recv_data.splitlines().encode('utf-8')
	# print(content_split)
	file_name =''
	if recv_data:
		# 正则表达式取值
		ret =re.match(r'[^/]+(/[^ ]*)',content_split[0])
		# 判断是否有值
		if ret:
			# 取值
			file_name= ret.group(1)
                        if file_name =="/":
				file.name ='/index.html' 
		try:
			# ./html表示当前路径下的文件夹
			f=open('./html'+file_name,'rb')
		except:
			# 存在没有找这个页面的可能性
			response = 'HTTP/1.1 404 NOT FOUND \r\n'
			response += '\r\n'
			response += '404 Not Found'
			new_client.send(responce.encode('utf-8'))

		else:
			file_content=f.read()
			f.close()
			# http 服务器回应客户端header和body

			response = 'HTTP/1.1 200 OK \r\n'
			response += '\r\n'
			# 把header发送给浏览器
			new_client.send(response,encode('utf-8'))
			# 把body发送给浏览器
			new_client.send(file_content)
			new_client.close()	

def main():
	# 创建套接字
	tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#绑定
	tcp_server_socket.bind(('',7895))
	#监听套接字
	tcp_server_socket.listen(12)
	while True:
		#accept创建套接字
		new_client,client_addr =tcp_server_socket.accept()
		p = multiprocessing.Process(target=server,args=(new_client,)
		p.start()		                            
		new_client.close() 

	 	#server(new_client)
	#关闭套接字
	tcp_server_socket.close()



if __name__ == '__main__':
	main()

