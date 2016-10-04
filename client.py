import sys
import time
import linecache
import socket
import random
from _thread import *
import os

filename=sys.argv[1]#get configuration filename from command line
linesNumber=sys.argv[2]#get line number
host=socket.gethostname()#host
#i=0 
l=0#lamport clock value
nodelist=[]#it stores all the active nodes' ports and its own port
##Read configuration file to find own port
lines=linecache.getlines(filename)
if int(linesNumber)>len(lines):
	print('This line number does not exist!')
	exit()
else:
	line=linecache.getline(filename,int(linesNumber))
	ID=line.split(' ')[0]
	port=int(line.split(' ')[1])
	nodelist.append(port)


##Send its own id and port to all nodes
for i in range(0,len(lines)):
	s=socket.socket()
	if lines[i].strip().split(' ')[1]!=str(port):
		if(s.connect_ex((host,int(lines[i].strip().split(' ')[1])))==0):
			nodelist.append(lines[i].strip().split(' ')[1])
			#print(len(nodelist))
			info='newnode '+str(ID)+' '+str(port)
			#print(info)
			s.send(bytes(info,'utf-8'))
			#print('sent')
	s.close()

def clientthread():
	global l#the lamport clock value
	def local_event():
		global l
		n=random.randrange(1,6)		
		l=l+n
		print('l '+str(n))
		#l=l+1
	def send_message():
		nodeID=0
		global nodelist
		global lines
		global l
		global ID
		s=socket.socket()
		ra=random.randrange(1,len(nodelist))
		nodeport=nodelist[ra]
		for i in range(0,len(lines)):
			temp = lines[i].strip().split(' ')
			if temp[1]==nodeport:
				nodeID=temp[0]
				
		if(s.connect_ex((host,int(nodeport)))==0):
			msg='message '+ID+' '+str(l)
			s.send(bytes(msg,'utf-8'))
			s.close()
			print('s '+str(nodeID)+' '+str(l))
			l=l+1
			#print('after sent: '+str(l))
		else:
			#print('whoops! This node has gone!')
			nodelist.remove(nodeport)
	for j in range(0,20):
		if(len(nodelist)>1):
			i=random.randrange(0,2)
			if i==0:
				local_event()
			else:
				send_message()
			#print('event1')
			time.sleep(0.5)
		else:
			local_event()
	
	time.sleep(2)
	os._exit(0)
	'''for i in range(0,5):
		#local_event()
		send_message()
		time.sleep(0.5)'''

def messagethread(msg):
	global l
	sender=str(msg.split(' ')[1])
	clock=int(msg.split(' ')[2])
	if clock>l:
		l=clock+1
	else:
		l=l+1
	print('r '+sender+' '+str(clock)+' '+str(l))         
#start_new_thread(messagethread,(msg))

s=socket.socket()					
s.bind((host,port))
s.listen(100)						
while True:
	buf=''
	conn, addr = s.accept()
	buf=str(conn.recv(1024))
	buf=buf.split("'")[1]
	print(buf)
	if('newnode' in buf):
		nodeID=buf.split(' ')[1]
		nodeport=buf.split(' ')[2]
		nodelist.append(nodeport)
		#print('length is '+str(len(nodelist)))
	if('yes' in buf):
		#print('okay')
		start_new_thread(clientthread,())
	if('message' in buf):
		start_new_thread(messagethread,(buf,))
