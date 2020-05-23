from sklearn import datasets
import numpy as np
import pandas as pd

iris = datasets.load_iris()
X = pd.DataFrame(iris.data[:, :2])  # we only take the first two features.
y = iris.target

def get_data():
    data = {}
    data['X'] = X
    data['y'] = y
    # data['iris'] = iris
    return data