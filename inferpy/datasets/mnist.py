"""MNIST handwritten digits dataset."""

from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt


def load_data(vectorize = True, num_instances=None, digits=[0,1,2,3,4,5,6,7,8,9]):

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    (x_train, y_train) = _preprocess_data(x_train, y_train, vectorize, num_instances, digits)
    (x_test, y_test) = _preprocess_data(x_test, y_test, vectorize, num_instances, digits)

    return (x_train, y_train), (x_test, y_test)


def _preprocess_data(x_data, y_data, vectorize = True, num_instances=None, digits=[0,1,2,3,4,5,6,7,8,9]):

    num_pixels = np.prod(np.shape(x_data)[1:])
    x_data = x_data[np.isin(y_data, digits)]
    y_data = y_data[np.isin(y_data, digits)]

    if num_instances is None:
        num_instances = len(x_data)

    y_data = y_data[:num_instances]
    x_data = x_data[:num_instances]

    if vectorize:
        x_data = np.reshape(x_data, (num_instances,num_pixels))  #serialize the data
        x_data = np.float32(x_data)

    return x_data, y_data



def plot_digits(data , grid = [3,3]):
    nx, ny = grid
    fig, ax = plt.subplots(nx, ny, figsize=(12, 12))
    fig.tight_layout(pad=0.3, rect=[0, 0, 0.9, 0.9])
    for x, y in [(i, j) for i in list(range(nx)) for j in list(range(ny))]:
        img_i = data[x + y * nx].reshape((28, 28))
        i = (x, y) if nx > 1 else y
        ax[i].imshow(img_i, cmap='gray')
    plt.show()