#!python3.6
# @ guliping

import selectors
import socket
import sys

# sel = selectors.DefaultSelector()

# sock = socket.socket()
# sock.setblocking(False)
# sel.register(sock, selectors.EVENT_READ, accept)
# sock.connect(("localhost",1234))

# def read(conn, mask):
# 	data = conn.recv(1000)  # Should be ready
# 	if data:
# 		print('echoing', repr(data), 'to', conn)
# 		conn.send(data)  # Hope it won't block
# 	else:
# 		print('closing', conn)
# 		sel.unregister(conn)
# 		conn.close()

# while True:
# 	print("wait...")
# 	events = sel.select(1)#设置超时等待时间
# 	for key, mask in events:
# 		print("select...")
# 		callback = key.data
# 		callback(key.fileobj, mask)

HOST = 'localhost'    # The remote host
PORT = 1234              # The same port as used by the server

print(socket.getaddrinfo("example.org", 80, proto=socket.IPPROTO_TCP))

print("client...")

s = None
#从域名获取到IP地址
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
	af, socktype, proto, canonname, sa = res
	try:
		s = socket.socket(af, socktype, proto)
	except OSError as msg:
		s = None
		continue
	try:
		s.connect(sa)
	except OSError as msg:
		s.close()
		s = None
		continue
	break
if s is None:
	print('could not open socket')
	sys.exit(1)

with s:
	s.sendall(b'Hello, world')
	data = s.recv(1024)
	print('Received', repr(data))

