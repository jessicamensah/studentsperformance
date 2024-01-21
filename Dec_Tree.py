import pandas as pd
import sklearn
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import *
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import matplotlib.image as pltimg
import pydotplus
from sklearn.datasets import load_iris
from sklearn.tree import plot_tree
import pymongo
#retrieve from MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client.StudentsPerformance
collection = database.StudentSample

df = pd.DataFrame(list(collection.find()))

#splitting data
print("Dataset Length: ", len(df)) #length of dataset
print("Dataset Shape: ", df.shape)  #clarifying how many rows and columns there are in the dataset
print("Dataset: ", df.head(100)) #checking if the first 100 can print in terminal

class StudentPerformanceClassifier:
    def __init__(self, data_file):
        self.df = data_file
        self.label_encoder = LabelEncoder()
        self.clf_entropy = None

    def preprocess_data(self): # string data which is being changed float by LabelEncoder
        self.df['gender'] = self.label_encoder.fit_transform(self.df['gender'])
        self.df['race/ethnicity'] = self.label_encoder.fit_transform(self.df['race/ethnicity'])
        self.df['parental level of education'] = self.label_encoder.fit_transform(self.df['parental level of education'])
        self.df['lunch'] = self.label_encoder.fit_transform(self.df['lunch'])
        self.df['test preparation course'] = self.label_encoder.fit_transform(self.df['test preparation course'])

    def train_classifer(self):
        X = self.df[['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'math score', 'reading score', 'writing score']]  
        # all other variables
        Y = self.df['test preparation course']  # Target variable
        #Splitting data into 4 parts for test & train
        X_train, X_test, y_train, y_test= train_test_split(X, Y, test_size= 0.3, random_state= 100) #30% of data picked randomly from the dataset
        #test and train using Entropy
        self.clf_entropy= DecisionTreeClassifier(criterion="entropy", random_state= 100, max_depth=3, min_samples_leaf=5)
        self.clf_entropy.fit(X_train, y_train)

        y_pred = self.clf_entropy.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

    def plot_decision_tree(self):
        plt.figure(figsize=(12, 8))
        plot_tree(self.clf_entropy, feature_names=['gender', 'race/ethnicity', 'parental level of education', 'lunch',  'math score', 'reading score', 'writing score'], filled=True, class_names=['not completed', 'completed'])  # Replace with your class names
        plt.show()

classifier = StudentPerformanceClassifier(df)






 

