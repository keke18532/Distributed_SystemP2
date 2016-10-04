import socket
import linecache


host=socket.gethostname()

lines=linecache.getlines('config.txt')
for i in range(0,len(lines)):
	s=socket.socket()
	if(s.connect_ex((host,int(lines[i].strip().split(' ')[1])))==0):
		print('okay')
		msg='yes'
		s.send(bytes(msg, 'utf-8'))
		print('sent')
	s.close()
	

	
