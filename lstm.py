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
from keras.layers import ConvLSTM2D
from keras.optimizers import Adam, SGD, RMSprop
from keras.utils import to_categorical
import matplotlib.pyplot as plt

import tensorflow as tf
'''
Run for GPU/CUDA ML, comment out if you dont have it configured.
'''
# gpu_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpu_devices[0], True)

## 7 gestures, windowsize = 50, overlap = 25
## 5 gestures, windowsize = 50, overlap = 25
dir_list = ["ready_data/x_train.txt", "ready_data/y_train.txt", "ready_data/x_test.txt", "ready_data/y_test.txt"]
## 5 gestures, windowsize = 50, overlap = 0
no_overlap = ["ready_data/no-overlap/x_train.txt", "ready_data/no-overlap/y_train.txt", "ready_data/no-overlap/x_test.txt", "ready_data/no-overlap/y_test.txt"]
no_overlap = ["ready_data/window-100/x_train.txt", "ready_data/window-100/y_train.txt", "ready_data/window-100/x_test.txt", "ready_data/window-100/y_test.txt"]

## 5 gestures, windowsize = 100, overlap = 50


num_gestures = 5
overlap = 0
window = 100
def load_dataset():

    if num_gestures == 7:
        trainxshape = (53466, 50, 6)
        trainyshape = (53466, 1)
        testxshape = (22911, 50, 6)
        testyshape = (22911, 1)
        directory = dir_list
    elif num_gestures == 5:
        if overlap == 0:
            trainxshape = (38190, 50, 6)
            trainyshape = (38190, 1)
            testxshape = (16365, 50, 6)
            testyshape = (16365, 1)
            directory = no_overlap

        elif overlap == 25 and window==100:
            trainxshape = (12730, 50, 6)
            trainyshape = (12730, 1)
            testxshape = (5455, 50, 6)
            testyshape = (5455, 1)
            directory = no_overlap
        else:
            trainxshape = (19095, 50, 6)
            trainyshape = (19095, 1)
            testxshape = (8185, 50, 6)
            testyshape = (8185, 1)
            directory = dir_list

    ## Load data previously saved as numpy text and reshape it to orginal form
    loaded_arr = np.loadtxt(directory[0])
    x_train = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // trainxshape[2], trainxshape[2])

    loaded_arr1 = np.loadtxt(directory[1])
    y_train = loaded_arr1

    loaded_arr2 = np.loadtxt(directory[2])
    x_test = loaded_arr2.reshape(loaded_arr2.shape[0], loaded_arr2.shape[1] // testxshape[2], testxshape[2])

    loaded_arr3 = np.loadtxt(directory[3])
    y_test = loaded_arr3

    print('##Before reshaping')
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    y_train = to_categorical(y_train, num_classes = num_gestures)
    y_test = to_categorical(y_test, num_classes = num_gestures)

    print('##After reshaping')
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    return x_train, y_train, x_test, y_test

def visualise(history):
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def evaluate_lstm(x_train, y_train, x_test, y_test, dropout):
    print("start evaluation!")
    LR = 0.0001
    verbose, epochs, batch_size = 1, 20, 64
    # timesteps = window size, #n_features = 6, n_outputs =
    n_timesteps, n_features, n_outputs = x_train.shape[1], x_train.shape[2], y_train.shape[1]
    model = Sequential()
    model.add(LSTM(100, input_shape=(n_timesteps, n_features), dropout=dropout))
    # model.add(LSTM(100, return_sequences=True, input_shape=(n_timesteps, n_features), dropout=dropout))
    # model.add(LSTM(10, return_sequences=True))
    # model.add(LSTM(64, return_sequences=True))
    # model.add(LSTM(32, return_sequences=True))
    # model.add(LSTM(100, dropout=dropout))
    model.add(Dropout(dropout))
    model.add(Dense(100, activation='relu'))
    # model.add(Dropout(0.3))
    # model.add(Dense(25, activation='relu'))
    model.add(Dense(n_outputs, activation='softmax'))
    opt = Adam(lr=LR)
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy', tf.keras.metrics.CategoricalAccuracy()])
    # kb.set_value(model.optimizer.learning_rate, LR)
    # fit network
    model.summary()
    # tf.keras.metrics.CategoricalAccuracy()
    # model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose,
                        validation_data=(x_test, y_test),  shuffle=True)
    ##plot
    visualise(history)
    # save model
    model.save('lstm_model1.pb')
    # evaluate model
    _, accuracy, cat_acc = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=verbose)
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
        ## use basic lstm
        score = evaluate_lstm(x_train, y_train, x_test, y_test, dropout)
        ##use ConvLSTM
        # score = evaluate_convlstm(x_train, y_train, x_test, y_test, dropout)
        score = score * 100.0
        print('>#%d: %.3f' % (r + 1, score))
        scores.append(score)
    # summarize results
    summarize_results(scores)


# run the experiment
run_experiment()
