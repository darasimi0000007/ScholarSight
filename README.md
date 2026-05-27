# Student Performance Predictor
Project Overview:
This project is a backend system focused on predicting the performance of a student according to his individual qualities.



MACHINE LEARNING DOCUMENTATION
Dataset Summary:
The Student Performance Dataset is a publicly available educational dataset from the UCI Machine Learning Repository. It contains detailed student records from Portuguese secondary schools, designed to support research on academic achievement modeling and predictive analytics.
Here is the link to the dataset: https://archive.ics.uci.edu/dataset/320/student+performance

Check the page for what each column means:
'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
       'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc',
       'Walc', 'health', 'absences', 'G1', 'G2', 'G3'

Column headers are the same for both datasets

Columns to drop for feature set: school, medu, fedu, Dalc, Walc, higher, Mjob, Fjob, reason, paid. This application does not require to know your school unlike the dataset that kept records on whether you attended Gabriel Pereira or Mousinho de Silveira school. 

each categorical column in both datasets and their respective encoder meaning using LabelEncoder
sex F-0, M-1
address U-1, R-0 (rural or urban)
famsize GT3-0, LE3-1 (greater than three or less than three)
pstatus T-1, A-0 (T for living together and A for Apart)
guardian father-0, mother-1
schoolsup no-0, yes-1
famsup no-0, yes-1
activities no-0, yes-1
nursery no-0, yes-1
internet no-0, yes-1
romantic no-0, yes-1
famrel very_poor = 1, poor = 2, average = 3, good = 4, very_good = 5
health very_poor = 1, poor = 2, average = 3, good = 4, very_good = 5
studytime 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, 4 - >10 hours
failures 0 - none, 1 - once, 2 - twice, 3 - thrice, 4 - more than three times
traveltime 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour
freetime very_low = 1, low = 2, average = 3, free = 4, very_free = 5
goout very_low = 1, low = 2, average = 3, free = 4, very_free = 5


Models Used:
RandomForestClassifier
GradientBoostingClassifier
Support Vector Machine


Went ahead to make use of Gradientoosting as the model for prediction. Tree model with the best ROC_AUC score out of the three




BACKEND DEVELOPMENT DOCUMENTATION
Using a SQLite database to store records of students with their respective predictions





"sex", "age", "address", "famsize", "Pstatus", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "activities", "nursery", "famrel", "health", "absences", "freetime", "goout", "internet", "romantic"

