import socket

tcp_socket = socket.socket()
tcp_socket.connect(("gateway", 514))
tcp_socket.send(b'hello, world!')
tcp_socket.close()
