from numpy import mean
from numpy import std
import numpy as np
from numpy import dstack
import keras.backend as kb
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import to_categorical

import tensorflow as tf
gpu_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpu_devices[0], True)

def load_dataset():
    trainxshape = (53466, 50, 6)
    trainyshape = (53466, 1)
    testxshape = (22904, 50, 6)
    testyshape = (22904, 1)

    ## Load data previously saved as numpy text and reshape it to orginal form
    loaded_arr = np.loadtxt("ready_data/x_train.txt")
    x_train = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // trainxshape[2], trainxshape[2])
    # %%

    loaded_arr1 = np.loadtxt("ready_data/y_train.txt")
    y_train = loaded_arr1  # .reshape(
    # loaded_arr1.shape[0], trainyshape[1])

    loaded_arr2 = np.loadtxt("ready_data/x_test.txt")
    x_test = loaded_arr2.reshape(loaded_arr2.shape[0], loaded_arr2.shape[1] // testxshape[2], testxshape[2])

    loaded_arr3 = np.loadtxt("ready_data/y_test.txt")
    y_test = loaded_arr3  # .reshape(
    # loaded_arr3.shape[0], loaded_arr3.shape[1])# // testyshape[2], testyshape[2])
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    # y_train = np.reshape((y_train[0]), 1)
    # y_test = np.reshape((y_test[0]), 1)

    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    return x_train, y_train, x_test, y_test

def evaluate_model(x_train, y_train, x_test, y_test, dropout):
    print("start evaluation!")
    LR = 0.0001
    verbose, epochs, batch_size = 1, 10, 64
    # timesteps = window size, #n_features = 6, n_outputs =
    n_timesteps, n_features, n_outputs = x_train.shape[1], x_train.shape[2], y_train.shape[1]
    model = Sequential()
    model.add(LSTM(100, input_shape=(n_timesteps, n_features), dropout=dropout))
    # model.add(LSTM(100, return_sequences=True, input_shape=(n_timesteps, n_features), dropout=dropout))
    # model.add(LSTM(10, return_sequences=True))
    # model.add(LSTM(64, return_sequences=True))
    # model.add(LSTM(32, return_sequences=True))
    # model.add(LSTM(100, dropout=dropout))
    model.add(Dropout(0.5))
    model.add(Dense(100, activation='relu'))
    # model.add(Dropout(0.3))
    # model.add(Dense(25, activation='relu'))
    model.add(Dense(n_outputs, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'],)
    # fit network
    kb.set_value(model.optimizer.learning_rate, LR)
    model.summary()

    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
    # save model
    model.save('lstm_model4')
    # evaluate model
    _, accuracy = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=verbose)
    return accuracy


# summarize scores
def summarize_results(scores):
    print(scores)
    m, s = mean(scores), std(scores)
    print('Accuracy: %.3f%% (+/-%.3f)' % (m, s))


# run an experiment
def run_experiment(repeats=1):
    # load data
    x_train, y_train, x_test, y_test = load_dataset()
    # repeat experiment
    dropout = 0.2
    # dropout = [0.0, 0.2, 0.3, 0.4, 0.5]
    scores = list()
    for r in range(repeats):
        score = evaluate_model(x_train, y_train, x_test, y_test, dropout)
        score = score * 100.0
        print('>#%d: %.3f' % (r + 1, score))
        scores.append(score)
    # summarize results
    summarize_results(scores)


# run the experiment
run_experiment()
