#Here, we are trying to classify music by genere using unsupervised learning
#We will trysome architecture, but the aim is to use some kind of recurrent 1d CNN and clusering onthe compressed layer
from tensorflow import keras
from tensorflow.keras import layers
from scipy.fft import fft, ifft
import tensorflow as tf

import tensorflow.keras.backend as K 

from os import listdir
from os.path import isfile, join

import numpy as np

import calendar
import time

import configparser

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

config = configparser.ConfigParser()
config.read(r'config.cfg')
fftLength = int(config.get('Dataset', 'fftLength'))
nFreq = int(config.get('Dataset', 'nFreq')) 
numFeatures = int(config.get('Dataset', 'numFeatures'))

batchSize = int(config.get('Model', 'batchSize'))
numEpochs = int(config.get('Model', 'epochs'))
modelName = config.get('Model', 'name')

if not modelName:
    ts = calendar.timegm(time.gmtime())
    modelName = "autocnn_"+str(ts)

trainFiles = ["ds/train/" + f for f in listdir("ds/train") if isfile(join("ds/train", f))]
testFiles = ["ds/test/" + f for f in listdir("ds/test") if isfile(join("ds/test", f))]

def get_input(path):
    data = np.load(path)
    return data

def dataGenerator(files, batchSize):
    while True:
        batch_paths = np.random.choice(a=files, size=batchSize)
        batch_inputs = []
        batch_outputs= []

        for input_path in batch_paths:
            inputData = get_input(input_path)
            batch_inputs  += [inputData]

        batch_x = np.array(batch_inputs)
        yield(batch_x, batch_x)



def root_mean_squared_error(y_true, y_pred):
            return K.sqrt(K.mean(K.square(y_pred - y_true))) 

def frobeniusDistance(yTrue, yPred):
    return tf.norm(yTrue - yPred) 

def modelDef(input_shape):
    input_img = keras.Input(shape=input_shape)
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D((4, 4), padding='same')(x)
    x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D((4, 4), padding='same')(x)
    x = layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)
    x = layers.Conv2D(2, (3, 3), activation='tanh', padding='same')(x)
    encoded = layers.MaxPooling2D((4, 4), padding='same')(x)

    x = layers.Conv2D(2, (3, 3), activation='relu', padding='same')(encoded)
    x = layers.UpSampling2D((4, 4))(x)
    x = layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    decoded = layers.Conv2D(3, (3, 3), activation='tanh', padding='same')(x)

    model = keras.Model(input_img, decoded)
    return model 


def main():
    model = modelDef(input_shape = (fftLength, nFreq, numFeatures))
    model.summary()

    trainGen = dataGenerator(trainFiles, batchSize)
    testGen = dataGenerator(testFiles, batchSize)

    #model.compile(optimizer='adam', loss=root_mean_squared_error)
    model.compile(optimizer='adam', loss=frobeniusDistance)
    model.fit(x = trainGen, validation_data = testGen, validation_steps=len(testFiles)/batchSize, steps_per_epoch=len(trainFiles)/batchSize, epochs=numEpochs)

    modelSave = keras.Model(model.input,model.get_layer('max_pooling2d_2').output)
    #Save model somewhere
    modelSave.save("models/" + modelName)
    #Test and save it in file
    results = model.evaluate(x = trainGen, batch_size = batchSize, steps = len(trainFiles)/batchSize)
    with open('results.txt', 'a') as f:
        print('[' + modelName + "]", file=f)
        print('final loss: ', results, file=f)

if __name__ == "__main__":
    main()
