from sklearn import datasets, svm, metrics
import tensorflow as tf
import tensorflow.keras as kr
from PIL import Image
import numpy as np
import base64

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    if req=='train\n':
        train()
        print('Modelo entrenado')
    else:
        
        binary = os.fsencode(req)
        

        image_64_decode = base64.decodebytes(binary) 

        result_file = 'image'
        with open(result_file, 'wb') as file_handler:
            file_handler.write(image_64_decode)

        Image.open(result_file).save(result_file + '.png', 'PNG')
        os.remove(result_file)

        image = Image.open(result_file + '.png')
        
        image = np.asarray(image)
        input_image=np.array([np.reshape(image,np.prod(image.shape)),])

        res = get_number(input_image)

        print('La imagen tiene el numero: ',res)
    pass
    

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
    model.fit(X, Y, epochs=100, verbose=0)

    model.save('num_detector.model')

def get_number(input_image):
    # carga modelo
    try:
        model = tf.keras.models.load_model('num_detector.model')
    except :
        train()
        print('Modelo entrenado')
        model = tf.keras.models.load_model('num_detector.model')

    Yr = model.predict(input_image)
    res = np.argmax(Yr[0])

    return res    
    
