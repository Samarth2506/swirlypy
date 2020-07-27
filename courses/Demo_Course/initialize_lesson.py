from sklearn import datasets
import numpy as np
import pandas as pd

iris_data = pd.read_csv("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

# Users creating lessons should add required variables to the data dict using get_data() function below. 
def get_data():
    data = {}
    data['iris_data'] = iris_data
    data['words'] = ['cat', 'window', 'defenestrate']
    return data