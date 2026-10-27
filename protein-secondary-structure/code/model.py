from data_prep import NaiveGeneSequenceTokenizer
from util import seq2ngrams, custome_accuracy, print_results, onehot_to_seq, get_results
from keras.utils import to_categorical
from keras.models import Model, Input, load_model
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional, concatenate, GRU, Conv1D, MaxPooling1D
from keras.initializers import glorot_normal
import matplotlib.pyplot as plt
import pandas as pd
from keras.regularizers import l2

class BaseLineNetwork:
	def __init__(self, train_data, tokenizer=NaiveGeneSequenceTokenizer, maxseq_len=512, n_grams=3, random_seed=123456, optimizer='rmsprop'):
		train_input_seqs, train_target_seqs = train_data[['input', 'expected']][(train_data.len <= maxseq_len)].values.T
		input_grams = self.prep_data_to_grams(train_input_seqs, n_grams)
		self.tokenizer = tokenizer(input_grams, target_seqs=train_target_seqs, maxseq_len=maxseq_len) 
		self.maxseq_len = maxseq_len
		self.n_words = self.tokenizer.get_num_words()
		self.n_tags = self.tokenizer.get_num_tags()
		self.n_grams = n_grams
		self.random_seed = random_seed

		self.create_network()
		self.optimizer = optimizer
		# Setting up the model with categorical x-entropy loss and the custom accuracy function as accuracy
		self.model.compile(optimizer = optimizer, loss = "categorical_crossentropy", metrics = [custome_accuracy])

		# Defining the decoders so that we can
		self.revsere_decoder_index = {value:key for key,value in self.tokenizer.tokenizer_decoder.word_index.items()}
		self.revsere_encoder_index = {value:key for key,value in self.tokenizer.tokenizer_encoder.word_index.items()}

	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		# Defining an embedding layer mapping from the words (n_words) to a vector of len 128
		x = Embedding(input_dim = self.n_words, output_dim = 128, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		# Defining a bidirectional LSTM using the embedded representation of the inputs
		x = Bidirectional(LSTM(units = 64, return_sequences = True, recurrent_dropout = 0.1))(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)

	def get_model_summary(self):
		self.model.summary()

	def prep_data_to_grams(self, data, n_grams):
		return seq2ngrams(data, n=n_grams)

	def prep_input_data(self, data):
		data = self.prep_data_to_grams(data, self.n_grams)
		return self.tokenizer.process_features(data)

	def prep_target_data(self, data):
		data = self.prep_data_to_grams(data, self.n_grams)
		return self.tokenizer.process_target(data)

	def fit(self, X_train, y_train, X_val, y_val, batch_size=128, epochs=5, verbose=1, tensorboard=None):
		X_train = self.prep_input_data(X_train)
		y_train = self.prep_target_data(y_train)
		X_val = self.prep_input_data(X_val)
		y_val = self.prep_target_data(y_val)
		# Training the model on the training data and validating using the validation set
		if tensorboard is None:
			self.model.fit(X_train, y_train, batch_size = batch_size, epochs = epochs, validation_data = (X_val, y_val), verbose = verbose)
		else:
			self.model.fit(X_train, y_train, batch_size = batch_size, epochs = epochs, validation_data = (X_val, y_val), verbose = verbose, callbacks=[tensorboard])

	def predict(self, data, type='processed'):
		if type!='processed':
			data = self.prep_input_data(data)
		y_pred = self.model.predict(data[:])
		return y_pred

	def output_kaggle_result(self, test_id, test_data, test_data_len):
		test_pred = self.predict(test_data, type='no')
		test_expected = [get_results(td, tp, self.revsere_decoder_index)[:tdl] for td, tp, tdl in zip(test_data, test_pred, test_data_len)]
		return pd.DataFrame({'id': test_id, 'expected': test_expected})

	def print_test_result(self, test_data):
		test_pred = self.predict(test_data, type='no')
		print(len(test_data))
		for i in range(len(test_data)):
			print_results(test_data[i], test_pred[i], self.revsere_decoder_index)

	def save_model(self, path='model/model.h5'):
		self.model.save(path)

	def load_model(self, path='model/model.h5'):
		self.model = load_model(path)
		self.model.compile(optimizer = self.optimizer, loss = "categorical_crossentropy", metrics = [custome_accuracy])


	def plot_loss_result(self):
		#plot training and validation loss
		loss = self.model.history['loss']
		val_loss = self.model.history['val_loss']
		epochs = range(1, len(loss) + 1)
		plt.plot(epochs, loss, 'bo', label='Training loss')
		plt.plot(epochs, val_loss, 'b', label='Validation loss')
		plt.title('Training and validation loss')
		plt.legend()

class BaseLineWithFeedForwardNetwork(BaseLineNetwork):
	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		# Defining an embedding layer mapping from the words (n_words) to a vector of len 128
		x = Embedding(input_dim = self.n_words, output_dim = 128, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		# Add FeedForward Layers
		x = Dense(256, activation="relu")(x)
		x = Dense(128, activation="relu")(x)
		# Defining a bidirectional LSTM using the embedded representation of the inputs
		x = Bidirectional(LSTM(units = 64, return_sequences = True, recurrent_dropout = 0.1))(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)


class StackedBidirectionalNetwork(BaseLineNetwork):
	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		# Defining an embedding layer mapping from the words (n_words) to a vector of len 128
		x = Embedding(input_dim = self.n_words, output_dim = 128, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		# Add FeedForward Layers
		x = Bidirectional(LSTM(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(x)
		# Defining a bidirectional LSTM using the embedded representation of the inputs
		x = Bidirectional(LSTM(units = 64, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)

class CRRNNNetwork(BaseLineNetwork):
	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		# Defining an embedding layer mapping from the words (n_words) to a vector of len 128
		x = Embedding(input_dim = self.n_words, output_dim = 128, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		c1 = Conv1D(filters = 128, kernel_size = 5, padding='SAME', activation='relu')(x)
		c2 = Conv1D(filters = 128, kernel_size = 3, padding='SAME', activation='relu')(x)

		merged = concatenate([c1, c2, x])

		first_bgru = Bidirectional(GRU(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(merged)

		merged_two = concatenate([first_bgru, merged])
		# Add FeedForward Layers
		x = Bidirectional(GRU(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(merged_two)

		x = Dense(256, activation="relu")(x)
		x = Dense(128, activation="relu")(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)

class ModifiedCRRNNNetwork(BaseLineNetwork):
	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		# Defining an embedding layer mapping from the words (n_words) to a vector of len 128
		x = Embedding(input_dim = self.n_words, output_dim = 128, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		c1 = Conv1D(filters = 128, kernel_size = 5, padding='SAME', activation='relu')(x)
		c2 = Conv1D(filters = 128, kernel_size = 3, padding='SAME', activation='relu')(x)

		merged = concatenate([c1, c2, x])

		first_bgru = Bidirectional(GRU(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(merged)

		merged_two = concatenate([first_bgru, merged])

		x = Conv1D(filters = 500, kernel_size = 1, padding='SAME', activation='relu')(merged_two)
		x = Bidirectional(GRU(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(x)

		merged_three = concatenate([first_bgru, x])

		x = Conv1D(filters = 500, kernel_size = 1, padding='SAME', activation='relu')(merged_three)
		x = Bidirectional(GRU(units = 128, return_sequences = True, dropout = 0.2, recurrent_dropout = 0.2))(x)

		x = Dense(256, activation="relu")(x)
		x = Dense(128, activation="relu")(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)

class FinalCRRNNNetwork(BaseLineNetwork):
	def create_network(self):
		input = Input(shape = (self.maxseq_len,))
		em = Embedding(input_dim = self.n_words, output_dim = 50, input_length = self.maxseq_len, embeddings_initializer=glorot_normal(seed=self.random_seed))(input)
		c1 = Conv1D(filters = 64, kernel_size = 5, padding='SAME', activation='relu', kernel_regularizer=l2(0.01), activity_regularizer=l2(0.01))(em)
		c2 = Conv1D(filters = 64, kernel_size = 3, padding='SAME', activation='relu', kernel_regularizer=l2(0.01), activity_regularizer=l2(0.01))(em)
		c3 = Conv1D(filters = 64, kernel_size = 7, padding='SAME', activation='relu', kernel_regularizer=l2(0.01), activity_regularizer=l2(0.01))(em)
		# Merge the embedding with the three local convolution branches.
		merged = concatenate([em, c1, c2, c3])

		first_bgru = Bidirectional(LSTM(units = 300, return_sequences = True, recurrent_dropout = 0.5))(merged)

		merged_two = concatenate([first_bgru, merged])

		x = Conv1D(filters = 300, kernel_size = 1, padding='SAME', activation='relu')(merged_two)
		x = Bidirectional(GRU(units = 300, return_sequences = True, recurrent_dropout = 0.5))(x)

		merged_three = concatenate([first_bgru, x])

		x = Conv1D(filters = 300, kernel_size = 1, padding='SAME', activation='relu')(merged_three)
		x = Bidirectional(GRU(units = 300, return_sequences = True, recurrent_dropout = 0.5))(x)

		x = concatenate([em, x])
		x = TimeDistributed(Dense(200, activation="relu", kernel_regularizer=l2(0.01), activity_regularizer=l2(0.01)))(x)
		x = TimeDistributed(Dense(200, activation="relu", kernel_regularizer=l2(0.01), activity_regularizer=l2(0.01)))(x)
		# A dense layer to output from the LSTM's64 units to the appropriate number of tags to be fed into the decoder
		y = TimeDistributed(Dense(self.n_tags, activation = "softmax"))(x)
		# Defining the model as a whole and printing the summary
		self.model = Model(input, y)
