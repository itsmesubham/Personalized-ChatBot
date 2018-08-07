from parsedata import *
from keras.preprocessing.text import text_to_word_sequence	
from keras.preprocessing.text import one_hot

wordset = set()
	
def addToset(xx):
	for i in range(1,len(xx)):
		wordset.add(xx[i])
def wordToTextSeq(xx,yy):
	X=[]
	Y=[]
	for i in range(0,len(xx)):
		x1 = xx[i]
		y1 = yy[i]
		px1= text_to_word_sequence(x1)
		py1= text_to_word_sequence(y1)
		
		addToset(px1)
		addToset(py1)

		X.append(px1)
		Y.append(py1)
	return X,Y
def oneHotEncoding(X,Y):
	vocab_size = len(wordset)
	xx=[]
	yy=[]
	for i in range(0,len(X)):
		r1=[]
		r2=[]
		for j in X[i]:
			r1.append(one_hot(j,round(vocab_size*1.3)))

		for j in Y[i]:
			r2.append(one_hot(j,round(vocab_size*1.3)))	
		
		xx.append(r1)
		yy.append(r2)
	return xx,yy


def getData():
	xx,yy = parseWhatsAppData("chat.txt")
	x1,y1=wordToTextSeq(xx,yy)
	X,Y=oneHotEncoding(x1,y1)
	print len(wordset)
	return X,Y,wordset

