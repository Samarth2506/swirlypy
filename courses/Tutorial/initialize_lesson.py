from sklearn import datasets
import numpy as np
import pandas as pd

# iris = datasets.load_iris()
# iris_data = pd.DataFrame(iris.data, columns=iris['feature_names'])  # we only take the first two features.
# target = iris.target

iris_data = pd.read_csv("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

# Users creating lessons should add required variables to the data dict using get_data() function below. 
def get_data():
    data = {}
    data['iris_data'] = iris_data
    return data