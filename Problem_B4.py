# ===================================================================================================
# PROBLEM B4
#
# Build and train a classifier for the BBC-text dataset.
# This is a multiclass classification problem.
# Do not use lambda layers in your model.
#
# The dataset used in this problem is originally published in: http://mlg.ucd.ie/datasets/bbc.html.
#
# Desired accuracy and validation_accuracy > 91%
# ===================================================================================================

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd


def solution_B4():
    bbc = pd.read_csv('https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/bbc-text.csv')

    # DO NOT CHANGE THIS CODE
    # Make sure you used all of these parameters or you can not pass this test
    vocab_size = 1000
    embedding_dim = 16
    max_length = 120
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = "<OOV>"
    training_portion = .8

    sentence = []
    labels=[]

    for index, row in bbc.iterrows():
        labels.append(row[0])
        sentence.append(row[1])

    training_size =int(len(sentence)*training_portion)


    # Using "shuffle=False"
    
    training_sentences, validation_sentences = sentence[: training_size], sentence[training_size: ]
    training_labels, validation_labels = labels[: training_size], labels[training_size: ] 

    # Fit your tokenizer with training data
    tokenizer =  Tokenizer(num_words = vocab_size, oov_token = oov_tok)
    tokenizer.fit_on_texts(training_sentences)
    train_sequences = tokenizer.texts_to_sequences(training_sentences)
    train_padded = pad_sequences(train_sequences, maxlen=max_length,padding=padding_type, truncating=trunc_type)

    validation_sequences = tokenizer.texts_to_sequences(validation_sentences)
    validation_padding = pad_sequences(validation_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(labels)
    training_label_seq = np.array(label_tokenizer.texts_to_sequences(training_labels))
    validation_labels_seq = np.array(label_tokenizer.texts_to_sequences(validation_labels))



    
    # You can also use Tokenizer to encode your label.

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(28, activation='relu'),
        # YOUR CODE HERE. DO not change the last layer or test may fail
        tf.keras.layers.Dense(6, activation='softmax')
    ])
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    # Make sure you are using "sparse_categorical_crossentropy" as a loss fuction
    history = model.fit(train_padded,
                        training_label_seq,
                        epochs=100,
                        validation_data=(validation_padding, validation_labels_seq))
    return model

    # The code below is to save your model as a .h5 file.
    # It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_B4()
    model.save("model_B4.h5")