import numpy as np
from sklearn import datasets, svm, metrics

import tensorflow as tf
import tensorflow.keras as kr



def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req

def train():
    digits = datasets.load_digits()

    images_and_labels = list(zip(digits.images, digits.target))
    X=[]
    Y=[]
    n=np.prod(images_and_labels[0][0].shape) #dimension in line image
    for index, (image, label) in enumerate(images_and_labels[:1000]):    
        _X=np.reshape(image,n) # get image in an array
        X.append(_X) # add array image to list of images
        _Y=np.zeros(10) # create the output of the NN
        _Y[label]=1 # ouput nn for images index
        Y.append(_Y) # add the oputput to the list of ouputs
    X=np.vstack(X)
    Y=np.vstack(Y)

    topology=[n,16,32,16,10]

    model = kr.Sequential()

    # Añadimos la capa 1
    model.add(tf.keras.layers.Flatten())

    # Añadimos la capa 2
    model.add(kr.layers.Dense(topology[1], activation='relu'))

    # Añadimos la capa 3
    model.add(kr.layers.Dense(topology[2], activation='relu'))

    # Añadimos la capa 4
    model.add(kr.layers.Dense(topology[3], activation='relu'))

    # Añadimos la capa 5
    model.add(kr.layers.Dense(topology[4], activation='sigmoid'))

    # Compilamos el modelo, definiendo la función de coste y el optimizador.
    model.compile(loss='mse', optimizer='adam', metrics=['acc'])

    # Y entrenamos al modelo. Los callbacks 
    model.fit(X, Y, epochs=100)

    model.save('num_detector.model')

def get_number():
    # carga modelo
    try:
        model = tf.keras.models.load_model('num_detector.model')
    except :
        train()
        model = tf.keras.models.load_model('num_detector.model')
    
    pass
