from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
database = client.StudentsPerformance
collection = database.StudentSample
 
df = pd.DataFrame(list(collection.find()))

prep_course_dict = {"none":0, "completed":1}
df['test preparation course'] = df['test preparation course'].map(prep_course_dict)

gender_dict = {"female":0, "male":1}
df['gender'] = df['gender'].map(gender_dict)

'''race_ethnicity_dict = {"group A":0, "group B":1, "group C":2, "group D":3, "group E":4}
raw_data['race/ethnicity'] = raw_data['race/ethnicity'].map(race_ethnicity_dict)'''

level_of_education_dict = {"some high school":0, "high school":1, "some college":2, "associate's degree":3, "bachelor's degree":4, "master's degree":5}
df['parental level of education'] = df['parental level of education'].map(level_of_education_dict)

lunch_dict = {"standard":0, "free/reduced":1}
df['lunch'] = df['lunch'].map(lunch_dict)

print(df)



