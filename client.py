import sys
import time
import linecache
import socket
import random
from _thread import *

filename=sys.argv[1]#get configuration filename from command line
linesNumber=sys.argv[2]#get line number
#ID=sys.argv[2]
host=socket.gethostname()#host
i=0 
#j=0
l=0#lamport clock value
nodelist=[]#it stores all the active nodes' ports and its own port
##Read configuration file to find own port
line=linecache.getline(filename,int(linesNumber))
ID=line.split(' ')[0]
port=int(line.split(' ')[1])
nodelist.append(port)
lines=linecache.getlines(filename)

##Send its own id and port to all nodes
for i in range(0,len(lines)):
	s=socket.socket()
	if lines[i].strip().split(' ')[1]!=str(port):
		if(s.connect_ex((host,int(lines[i].strip().split(' ')[1])))==0):
			nodelist.append(lines[i].strip().split(' ')[1])
			info=lines[i].strip().split(' ')[0]+' '+lines[i].strip().split(' ')[1]
			s.send(bytes(info,'utf-8'))
			print('sent')
	s.close()

def clientthread():
	global l#the lamport clock value
	def local_event():
		global l
		n=random.randrange(1,6)		
		l=l+n
		#print('l '+str(l))
		#l=l+1
	def send_message():
		nodeID=0
		global nodelist
		global lines
		global l
		s=socket.socket()
		ra=random.randrange(0,len(nodelist))
		nodeport=nodelist[ra]
		for i in range(0,len(lines)):
			temp = lines[i].strip().split(' ')
			if temp[1]==nodeport:
				nodeID=temp[0]
                
		s.connect(host,nodeport)
		msg='message '+ID+' '+l
		#flag
		s.send(bytes(msg,'utf-8'))
		s.close()
		l=l+1
		print('s '+nodeID+' '+l)
	for i in range(0,5):
		local_event()
	

s=socket.socket()					
s.bind((host,port))
s.listen(100)						
while True:
	buf=''
	conn, addr = s.accept()
	buf=conn.recv(1024)
	
	print(str(buf))
	if('yes' in str(buf)):
		print('okay')
		start_new_thread(clientthread,())
