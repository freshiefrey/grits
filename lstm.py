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
import os

import tensorflow as tf
'''
Run for GPU/CUDA ML, comment out if you dont have it configured.
'''
gpu_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpu_devices[0], True)

## 7 gestures, windowsize = 50, overlap = 25
dir_list = ["ready_data/x_train.txt", "ready_data/y_train.txt", "ready_data/x_test.txt", "ready_data/y_test.txt"]

## 5 gestures, windowsize = 50, overlap = 25
window_50_25 = ["ready_data/window-50-25/x_train.txt", "ready_data/window-50-25/y_train.txt",
                 "ready_data/window-50-25/x_test.txt", "ready_data/window-50-25/y_test.txt"]

## 5 gestures, windowsize = 50, overlap = 0
no_overlap_50 = ["ready_data/no-overlap-50/x_train.txt", "ready_data/no-overlap-50/y_train.txt",
                  "ready_data/no-overlap-50/x_test.txt", "ready_data/no-overlap-50/y_test.txt"]

## 5 gestures, windowsize = 100, overlap = 0
no_overlap_100 = ["ready_data/no-overlap-100/x_train.txt", "ready_data/no-overlap-100/y_train.txt",
                 "ready_data/no-overlap-100/x_test.txt", "ready_data/no-overlap-100/y_test.txt"]

## 5 gestures, windowsize = 100, overlap = 25
window_100_25 = ["ready_data/window-100-25/x_train.txt", "ready_data/window-100-25/y_train.txt",
                 "ready_data/window-100-25/x_test.txt", "ready_data/window-100-25/y_test.txt"]

## 5 gestures, windowsize = 100, overlap = 50
window_100_50 = ["ready_data/window-100-50/x_train.txt", "ready_data/window-100-50/y_train.txt",
                 "ready_data/window-100-50/x_test.txt", "ready_data/window-100-50/y_test.txt"]

## 5 gestures, windowsize = 100, overlap = 50


num_gestures = 4
overlap = 25
window = 50
data_columns = 6

def load_dataset():
    if num_gestures == 7:
        directory = dir_list

    elif num_gestures == 4 or num_gestures == 5:

        if overlap == 0 and window == 50:
            directory = no_overlap_50

        elif overlap == 25 and window == 50:
            directory = window_50_25

        elif overlap == 0 and window == 100:
            directory = no_overlap_100

        elif overlap == 25 and window == 100:
            directory = window_100_25

        elif overlap == 50 and window == 100:
            directory = window_100_50


    ## Load data previously saved as numpy text and reshape it to orginal form
    loaded_arr = np.loadtxt(directory[0])
    x_train = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // data_columns, data_columns)

    loaded_arr1 = np.loadtxt(directory[1])
    y_train = loaded_arr1

    loaded_arr2 = np.loadtxt(directory[2])
    x_test = loaded_arr2.reshape(loaded_arr2.shape[0], loaded_arr2.shape[1] // data_columns, data_columns)

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

    ## Uncomment below and comment out lstm to use Convolution LSTM
    # n_steps, n_length = 4, 25
    # x_train = x_train.reshape((x_train.shape[0], n_steps, 1, n_length, n_features))
    # x_test = x_test.reshape((x_test.shape[0], n_steps, 1, n_length, n_features))
    # model.add(ConvLSTM2D(filters=32, kernel_size=(1, 3), activation='relu',
                         # input_shape=(n_steps, 1, n_length, n_features)))
    model.add(Dropout(dropout))
    # model.add(Flatten())
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
    if not os.path.exists('lstm_models'):
        os.makedirs('lstm_models')
    model_name = 'lstm_models/lstm_model_' + str(window) + '_' + str(overlap)
    model.save(model_name)
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
