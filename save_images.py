import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
import cv2
digits = datasets.load_digits()
images_and_labels = list(zip(digits.images, digits.target))

for index, (image, label) in enumerate(images_and_labels[1000:1100]):
    image=(image/np.max(image))*(2**8)
    name = 'example-images/{:d}.png'.format(index)
    cv2.imwrite(name, image)