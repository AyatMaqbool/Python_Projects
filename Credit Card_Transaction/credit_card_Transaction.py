# -*- coding: utf-8 -*-
"""Credit_Card_Assignment_Final

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LqLpU4haKK1QTpSFpTE7qncSqotayzXh

Importing the descripencies
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

#Loading the dataset to a Pandas DataFrame
from google.colab import drive
drive.mount('/content/drive')

path="/content/drive/MyDrive/CreditCardData.csv"
df=pd.read_csv(path)

# Replace incorrect values with the correct date
df['Date'] = df['Date'].replace({'15-Oct-20': '14-Oct-20', '16-Oct-20': '14-Oct-20'})

# Verify the changes
df['Date'].unique()

# Step 1: Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load the data
path = "/content/drive/MyDrive/CreditCardData.csv"
df = pd.read_csv(path)

# Step 3: Exclude 'Transaction ID' column
features = ['Date', 'Day of Week', 'Time', 'Type of Card', 'Entry Mode',
            'Type of Transaction', 'Merchant Group', 'Country of Transaction',
            'Shipping Address', 'Country of Residence', 'Gender', 'Bank', 'Fraud']

# Create a subset of the data with selected features
subset_data = df[features]

# Step 4: Set up a grid for subplots
fig, axes = plt.subplots(nrows=len(features)//2, ncols=2, figsize=(10, 15))

# Flatten the axes for easy iteration
axes = axes.flatten()

# Step 5: Create count plots for each feature
for i, feature in enumerate(features[:-1]):  # Exclude 'Fraud' column
    sns.countplot(x=feature, hue='Fraud', data=subset_data, ax=axes[i])

    # Set title and adjust layout
    axes[i].set_title(f'{feature} vs Fraud')
    axes[i].tick_params(axis='x', rotation=45)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')
    axes[i].legend(title='Fraud', labels=['Normal', 'Fraudulent'])

# Adjust layout
plt.tight_layout()

# Remove empty subplots (if any)
if len(features) % 2 != 0:
    fig.delaxes(axes[-1])

# Show the plot
plt.show()

df.head()

df.tail()

#Dataset Informations
df.info()

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

categorical_columns = ['Day of Week','Type of Card', 'Entry Mode', 'Type of Transaction',
                       'Merchant Group', 'Country of Transaction',
                       'Shipping Address', 'Country of Residence',
                       'Gender', 'Bank']

for column in categorical_columns:
  df[column] = label_encoder.fit_transform(df[column])

df

#Data Cleaning and Validation
#Checking of missing values
print(df.isnull().sum())

#Handling of missing values
# Convert 'Amount' to numeric format and handle missing values
df['Amount'] = df['Amount'].str.replace('£', '').str.replace(',', '').astype(float)
df['Amount'].fillna(df['Amount'].median(), inplace=True)

mode_merchant_group = df['Merchant Group'].mode()[0]
df['Merchant Group'].fillna(mode_merchant_group, inplace=True)

df['Shipping Address'].fillna('Unknown', inplace=True)

mode_gender = df['Gender'].mode()[0]
df['Gender'].fillna(mode_gender, inplace=True)

#Rechecking of Missing values
print(df.isnull().sum())

sns.relplot(x= 'Amount', y='Time', hue='Fraud',data=df)

count_Fraud=pd.value_counts(df['Fraud'],sort=True)
count_Fraud.plot(kind='bar',rot=0)
LABELS= ["Normal","Fraud"]
plt.title=("Transaction Class Distribtion")
plt.xticks(range(2), LABELS)

plt.xlabel("Class")

plt.ylabel("Frequency")

#Correlation Matrix
corr=df.corr()
plt.figure(figsize=(15,10))
sns.heatmap(corr,annot=True, cmap='coolwarm')

#Distribution of Legit transactions & fraudulent transactions
df['Fraud'].value_counts()

"""This dataset is highly unbalanced

0---> Normal Transactions

1--->Fraudulent Transactions
"""

#Separting the data for analysis
Normal=df[df.Fraud==0]
Fraudulent=df[df.Fraud==1]

print(Normal.shape)
print(Fraudulent.shape)

#Statistical Measures of the data
Normal.Amount.describe()

Fraudulent.Amount.describe()

#compare the values of both the transactions
df.groupby('Fraud').mean()

"""Under Sampling

Build a sample Data Set containing similar distribution for Noram Transaction and Fraudulent Transaction

No of Fraudulent Transactions-->7195
"""

Fraudulent_sample=Normal.sample(n=7195)

"""Concatenating two DataFrames"""

newdataset=pd.concat([Fraudulent_sample,Fraudulent],axis=0)

newdataset.head()

newdataset.tail()

newdataset['Fraud'].value_counts()

newdataset.groupby('Fraud').mean()

"""Spliting the data into Features and Traget"""

X=newdataset.drop(columns=['Transaction ID','Date','Fraud'],axis=1)
Y=newdataset['Fraud']

print(X)

print(Y)

"""Split the data into Training data and Testing data"""

X_train, X_test, Y_train, Y_test= train_test_split(X,Y, test_size=0.2, stratify=Y,random_state=2)

print(X.shape,X_train.shape,X_test.shape)

"""Model Training

Logistic Regression
"""

model=LogisticRegression()

#training the logistic regression model with trainning data
model.fit(X_train,Y_train)

"""Model Evaluation"""

from os import access
#Accuracy score on Training Data
X_train_prediction=model.predict(X_train)
training_data_accuracy=accuracy_score(X_train_prediction,Y_train)

print('Accuracy on Training data: ',training_data_accuracy)

#Accuracy on Testing Data
X_test_prediction=model.predict(X_test)
testing_data_accuracy=accuracy_score(X_test_prediction,Y_test)

print('Accuracy on Testing data: ',testing_data_accuracy)

from sklearn.metrics import confusion_matrix, classification_report

# Calculate Confusion Matrix
conf_matrix_train = confusion_matrix(Y_train, X_train_prediction)

# Generate Classification Report
class_report_train = classification_report(Y_train, X_train_prediction)

print("Confusion Matrix (Training Data):")
print(conf_matrix_train)

print("\nClassification Report (Training Data):")
print(class_report_train)

# Calculate Confusion Matrix
conf_matrix_test = confusion_matrix(Y_test, X_test_prediction)

# Generate Classification Report
class_report_test = classification_report(Y_test, X_test_prediction)

print("Confusion Matrix (Testing Data):")
print(conf_matrix_test)

print("\nClassification Report (Testing Data):")
print(class_report_test)

"""Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

# Create a RandomForestClassifier instance
rf_model = RandomForestClassifier(random_state=2)

# Train the model on the training data
rf_model.fit(X_train, Y_train)

# Predict on the training data
Y_train_pred = rf_model.predict(X_train)

# Predict on the testing data
Y_test_pred = rf_model.predict(X_test)

# Evaluate the model
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Accuracy on training data
train_accuracy = accuracy_score(Y_train, Y_train_pred)

# Accuracy on testing data
test_accuracy = accuracy_score(Y_train, Y_train_pred)
# Confusion matrix on training data
confusion_mat = confusion_matrix(Y_train, Y_train_pred)

# Classification report on training data
class_report = classification_report(Y_train, Y_train_pred)

# Print the results
print(f"Accuracy on Training Data: {train_accuracy:.4f}")
print(f"Accuracy on Testing Data: {test_accuracy:.4f}")
print("\nConfusion Matrix:")
print(confusion_mat)
print("\nClassification Report:")
print(class_report)


# Confusion matrix on testing data
confusion_mat = confusion_matrix(Y_test, Y_test_pred)

# Classification report on testing data
class_report = classification_report(Y_test, Y_test_pred)

# Print the results
print(f"Accuracy on Training Data: {train_accuracy:.4f}")
print(f"Accuracy on Testing Data: {test_accuracy:.4f}")
print("\nConfusion Matrix:")
print(confusion_mat)
print("\nClassification Report:")
print(class_report)