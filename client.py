import socket

tcp_socket = socket.socket()
tcp_socket.connect(("localhost", 2000))
tcp_socket.send(b'hello, world!')
tcp_socket.close()
