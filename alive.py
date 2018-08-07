
from pickle import load
from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.callbacks import ModelCheckpoint
from numpy import array
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def load_sentences(filename):
	return load(open(filename,"rb"))

def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer
def max_length(lines):
	mx =0
	for line in lines:
		mx = max(mx,len(line.split()));
	return mx
def encode_sequences(tokenizer,length,lines):
	X=tokenizer.texts_to_sequences(lines)
	X=pad_sequences(X,maxlen=length,padding='post')
	return X
def encode_output(sequences, vocab_size):
	ylist = list()
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size)
		ylist.append(encoded)
	y = array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None	

def define_model(src_vocab,tar_vocab,src_timestamp,tar_timestamp,n_units):
	model=Sequential()
	model.add(Embedding(src_vocab,n_units,input_length=src_timestamp,mask_zero=True))
	model.add(LSTM(n_units))
	model.add(RepeatVector(tar_timestamp))
	model.add(LSTM(n_units,return_sequences=True))
	model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
	return model

def evaluate_model(model, tokenizer, sources, raw_dataset):
	actual, predicted = list(), list()
	for i, source in enumerate(sources):
		# translate encoded source text
		source = source.reshape((1, source.shape[0]))
		translation = predict_sequence(model,tokenizer, source)
		raw_target, raw_src = raw_dataset[0][i],raw_dataset[1][i]
		if i < 10:	
			print('src=[%s], target=[%s], predicted=[%s]' % (raw_src, raw_target, translation))
		actual.append(raw_target.split())
		predicted.append(translation.split())
data = load_sentences("chat.dat")
his_tokenizer = create_tokenizer(data[0])
his_vocab_size = len(his_tokenizer.word_index)+1
X=data[0]
#print X[1].split()
his_length = max_length(X)
#print "his vocab size ",his_vocab_size," his max length ",his_length
her_tokenizer = create_tokenizer(data[1])
her_vocab_size = len(her_tokenizer.word_index)+1
her_length =max_length(data[1])
lim=400
X=["hello"]
trainX=encode_sequences(his_tokenizer,his_length,data[0])
trainY=encode_sequences(her_tokenizer,her_length,data[1])
trainX=trainX[0:lim]
trainY=trainY[0:lim]
trainY=encode_output(trainY[0:lim],her_vocab_size)
# load model
model = load_model('m.h5')
data1=[]

data1.append(X)
data1.append(data[1])
#print len(data1),len(data1[0]),len(data1[1])
evaluate_model(model,his_tokenizer,trainX,data1);


	
