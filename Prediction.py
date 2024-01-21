import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client.StudentsPerformance
collection = database.StudentSample

df = pd.DataFrame(list(collection.find()))

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

    def train_classifier(self):
        X = self.df[['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'math score', 'reading score', 'writing score']]  # all other variables
        Y = self.df['test preparation course']  # Target variable
        #Splitting data into 4 parts for test & train
        X_train, X_test, y_train, y_test= train_test_split(X, Y, test_size= 0.3, random_state= 100) #30% of data picked randomly from the datas
        #test and train using Entropy
        self.clf_entropy= DecisionTreeClassifier(criterion="entropy", random_state= 100, max_depth=3, min_samples_leaf=5)
        model = self.clf_entropy.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
        return model

classifier = StudentPerformanceClassifier(df)
classifier.preprocess_data()
classifier.train_classifier()
