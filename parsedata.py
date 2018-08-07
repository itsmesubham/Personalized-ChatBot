from pickle import dump
from pickle import load
from numpy.random import shuffle

def readfromfile(file):
	""" Converts raw data to meaningful form
	"""
	line = file.readline()
	name1 = []
	msg  = []
		#print "name,message,"
	while 1==1:
		line = file.readline()
		if len(line)==0:
			break
		temp = line.find(":")
		justMessage=line.find(":",temp+1,)
		justName = line.find("-")
		name = line[justName+1:justMessage-1]
		
		name=lstrip(name)
		name.rstrip("\n\r")
		if len(name)>0 and name[0]=='N':
			name="her"
		else:
			name="him"
		name1.append(name)
		message = line[justMessage+1:]
		message=lstrip(message)
		message.rstrip("\n\r")
		msg.append(message)

	return name1,msg



def lstrip(str1):
	"""function to trim leading spaces
	"""
	i =0;
	idx=0;
	while i<len(str1):
		if(str1[i]!=' '):
			idx=i;
			break;
		
		i=i+1;
	str1=str1[idx:]
	return str1
def reqres(name1,msg):
	"""
		convert messages to 
		message sent and response received from that message
		
	"""
	prevName = name1[0]
	X=[]
	Y=[]
	f=1;
	s=msg[0]
	start=3;
	f=0;
	while start<len(msg): 
		name = name1[start];
		if f==0:
			message=""
			while start<len(name1) and name==name1[start] :
				message=message+msg[start]
				start=start+1
			X.append(message)
			f=1
		else:
			message=""
			while start<len(name1) and name==name1[start]:
				message=message+msg[start]
				start=start+1;
			Y.append(message)
			f=0
	return X,Y

def parseWhatsAppData(filename):
	""""function to parse whatsapp data"""
	file = open(filename)
	name1,msg=readfromfile(file)
	return reqres(name1,msg)

def saveData(data,filename):
	dump(data,open(
save=[]filename,'wb'))
	print('Saved: %s'%filename)
	
def test():
	X,Y=parseWhatsAppData("chat.txt")
	for i in range(1,10):
		print "req: ",X[i]," res:",Y[i]
X,Y=parseWhatsAppData("chat.txt")
save=[]
XX=[]
YY=[]
for i in range(0,len(X)):
	msg = X[i]
	msg2=Y[i]
	if Y[i]=="Hmmm":
		continue
	if len(msg)>50 or len(msg2)>50:
		continue
	else:
		XX.append(X[i]);
		YY.append(Y[i]);
		
save.append(YY)
save.append(XX)
shuffle(save)
saveData(save,"chat.dat")
