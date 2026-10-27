from keras.preprocessing import text, sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from base import AbstractTokenizer

class NaiveGeneSequenceTokenizer(AbstractTokenizer):
	def __init__(self, input_grams, target_seqs=None, maxseq_len=512):
		# Initializing and defining the tokenizer encoders and decoders based on the train set
		self.tokenizer_encoder = Tokenizer()
		self.tokenizer_encoder.fit_on_texts(input_grams)
		if target_seqs is not None:
			self.tokenizer_decoder = Tokenizer(char_level = True)
			self.tokenizer_decoder.fit_on_texts(target_seqs)
		self.maxseq_len = maxseq_len

	def process_features(self, input_grams):
		# Using the tokenizer to encode and decode the sequences for use in training
		input_data = self.tokenizer_encoder.texts_to_sequences(input_grams)
		input_data = sequence.pad_sequences(input_data, maxlen = self.maxseq_len, padding = 'post')
		return input_data

	def process_target(self, target_seqs):
		if self.tokenizer_decoder is not None:
			target_data = self.tokenizer_decoder.texts_to_sequences(target_seqs)
			target_data = sequence.pad_sequences(target_data, maxlen = self.maxseq_len, padding = 'post')
			target_data = to_categorical(target_data)
			return target_data

	def get_num_words(self):
		return len(self.tokenizer_encoder.word_index) + 1

	def get_num_tags(self):
		return len(self.tokenizer_decoder.word_index) + 1



