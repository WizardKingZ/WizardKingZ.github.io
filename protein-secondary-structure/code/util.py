import tensorflow as tf
import numpy as np
from keras import backend as K

def custome_accuracy(y_true, y_pred):
	"""
	calculate accuracy
	---
	This is a computational graph
	"""
	y = tf.argmax(y_true, axis =- 1)
	y_ = tf.argmax(y_pred, axis =- 1)
	mask = tf.greater(y, 0)
	return K.cast(K.equal(tf.boolean_mask(y, mask), tf.boolean_mask(y_, mask)), K.floatx())

def onehot_to_seq(oh_seq, index):
	"""
	map sequence to a one-hot encoding
	"""
	s = ''
	for o in oh_seq:
		i = np.argmax(o)
		if i != 0:
			s += index[i]
		else:
			break
	return s

def get_results(x, y_, revsere_decoder_index):
	return str(onehot_to_seq(y_, revsere_decoder_index).upper())

def print_results(x, y_, revsere_decoder_index):
	"""
	print result
	"""
	print(str(onehot_to_seq(y_, revsere_decoder_index).upper()))

def seq2ngrams(seqs, n = 3):
	"""
	Computes and returns the n-grams of a particualr sequence, defaults to trigrams
	"""
	return np.array([",".join([seq[i : i + n] for i in range(len(seq))]) for seq in seqs])
