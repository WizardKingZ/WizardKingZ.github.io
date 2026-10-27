import pandas as pd
from model import FinalCRRNNNetwork
from sklearn.model_selection import train_test_split
from keras.callbacks import TensorBoard
from time import time
from keras.optimizers import Adam

tensorboard = TensorBoard(log_dir="logs/{}".format(time()), histogram_freq=2,
    write_graph=True)

train_df = pd.read_csv('dataset/train.csv')
test_df = pd.read_csv('dataset/test.csv')

train_input_seqs, train_target_seqs = train_df[['input', 'expected']].values.T

network = FinalCRRNNNetwork(train_df, n_grams=1, optimizer=Adam(lr=0.0004), maxseq_len=512)
network.get_model_summary()
"""
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_1 (InputLayer)            (None, 512)          0                                            
__________________________________________________________________________________________________
embedding_1 (Embedding)         (None, 512, 128)     2816        input_1[0][0]                    
__________________________________________________________________________________________________
conv1d_1 (Conv1D)               (None, 512, 128)     82048       embedding_1[0][0]                
__________________________________________________________________________________________________
conv1d_2 (Conv1D)               (None, 512, 128)     49280       embedding_1[0][0]                
__________________________________________________________________________________________________
concatenate_1 (Concatenate)     (None, 512, 384)     0           conv1d_1[0][0]                   
                                                                 conv1d_2[0][0]                   
                                                                 embedding_1[0][0]                
__________________________________________________________________________________________________
bidirectional_1 (Bidirectional) (None, 512, 400)     702000      concatenate_1[0][0]              
__________________________________________________________________________________________________
concatenate_2 (Concatenate)     (None, 512, 784)     0           bidirectional_1[0][0]            
                                                                 concatenate_1[0][0]              
__________________________________________________________________________________________________
conv1d_3 (Conv1D)               (None, 512, 500)     392500      concatenate_2[0][0]              
__________________________________________________________________________________________________
bidirectional_2 (Bidirectional) (None, 512, 400)     841200      conv1d_3[0][0]                   
__________________________________________________________________________________________________
concatenate_3 (Concatenate)     (None, 512, 800)     0           bidirectional_1[0][0]            
                                                                 bidirectional_2[0][0]            
__________________________________________________________________________________________________
conv1d_4 (Conv1D)               (None, 512, 500)     400500      concatenate_3[0][0]              
__________________________________________________________________________________________________
bidirectional_3 (Bidirectional) (None, 512, 400)     841200      conv1d_4[0][0]                   
__________________________________________________________________________________________________
dense_1 (Dense)                 (None, 512, 256)     102656      bidirectional_3[0][0]            
__________________________________________________________________________________________________
dense_2 (Dense)                 (None, 512, 128)     32896       dense_1[0][0]                    
__________________________________________________________________________________________________
time_distributed_1 (TimeDistrib (None, 512, 9)       1161        dense_2[0][0]                    
==================================================================================================
Total params: 3,448,257
Trainable params: 3,448,257
Non-trainable params: 0
__________________________________________________________________________________________________
"""

X_train, X_val, y_train, y_val = train_test_split(train_input_seqs, train_target_seqs, test_size = .1, random_state = 123456)
network.fit(X_train, y_train, X_val, y_val, epochs=20, batch_size=32)

from sklearn.model_selection import KFold
kfold = KFold(n_splits=10, shuffle=True, random_state=123456)
i = 0
for train, test in kfold.split(train_input_seqs.reshape(-1, 1), train_target_seqs.reshape(-1, 1)):
  network.fit(train_input_seqs[train], train_target_seqs[train], train_input_seqs[test], train_target_seqs[test], epochs=1, batch_size=96, tensorboard=tensorboard)
  network.save_model(path='FinalCRRNN_model_v2{}.h5'.format(i))
  i += 1
"""
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 386s 65ms/step - loss: 0.6430 - custome_accuracy: 0.6314 - val_loss: 0.7077 - val_custome_accuracy: 0.5952
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 387s 66ms/step - loss: 0.6443 - custome_accuracy: 0.6313 - val_loss: 0.6296 - val_custome_accuracy: 0.6306
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 384s 65ms/step - loss: 0.6426 - custome_accuracy: 0.6320 - val_loss: 0.6067 - val_custome_accuracy: 0.6460
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 383s 65ms/step - loss: 0.6382 - custome_accuracy: 0.6337 - val_loss: 0.6190 - val_custome_accuracy: 0.6413
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 384s 65ms/step - loss: 0.6287 - custome_accuracy: 0.6378 - val_loss: 0.6514 - val_custome_accuracy: 0.6374
Train on 5909 samples, validate on 657 samples
Epoch 1/1
5909/5909 [==============================] - 386s 65ms/step - loss: 0.6259 - custome_accuracy: 0.6395 - val_loss: 0.6258 - val_custome_accuracy: 0.6482
Train on 5910 samples, validate on 656 samples
Epoch 1/1
5910/5910 [==============================] - 381s 64ms/step - loss: 0.6236 - custome_accuracy: 0.6413 - val_loss: 0.6181 - val_custome_accuracy: 0.6487
Train on 5910 samples, validate on 656 samples
Epoch 1/1
5910/5910 [==============================] - 380s 64ms/step - loss: 0.6203 - custome_accuracy: 0.6435 - val_loss: 0.5989 - val_custome_accuracy: 0.6523
Train on 5910 samples, validate on 656 samples
Epoch 1/1
5910/5910 [==============================] - 377s 64ms/step - loss: 0.6152 - custome_accuracy: 0.6464 - val_loss: 0.5906 - val_custome_accuracy: 0.6580
Train on 5910 samples, validate on 656 samples
Epoch 1/1
5910/5910 [==============================] - 381s 64ms/step - loss: 0.6073 - custome_accuracy: 0.6505 - val_loss: 0.6164 - val_custome_accuracy: 0.6468
"""

network.save_model(path='FinalCRRNN_model_v2.h5')
kaggle_result = network.output_kaggle_result(test_df.id, test_df.input, test_df.len)
kaggle_result.to_csv('kaggle_output_FinalCRRNN.csv', index=False)

