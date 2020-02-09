'''
Rush Weigelt
Feb 2020
This script is to create Django objects out of our ML models
Lots of helper functions
'''

#Django imports
from django.db import models
#ML imports
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import cross_validate, train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn import metrics
from pymongo import MongoClient
import numpy as np
from joblib import load
#from tensorflow.python.keras.models import load_model, model_from_json
from keras.utils import CustomObjectScope

#Hardcoded function to open our client and look at a specific collection to train our model
#Returns a Pandas Dataframe Object
def read_mongo_data(database, collection):
    client = MongoClient('bvm15.cci.drexel.edu')
    db = client[database]
    df = db[collection]
    df = pd.DataFrame(list(df.find()))
    return df
    #This did not work, and did not seem neccesary for the amt of data we have
    #Create query to the specific DB and Collection
    #cursor = db[collection].find(query)
    #print(cursor)
    #Make cursor into DF
    #df = pd.DataFrame(list(cursor))
    #Delete ID col
    #if no_id:
        #del df['_id']
    #return df

#Helper function to be used after read_mongo_data: fill nas, convert all columns from strings to numberic
#Returns two pandas dataframe, one a df of our features, the other of our labels
def clean_data_strings_to_ints(dataframe):
    dataframe.fillna(0, inplace=True)
    fieldnames_list = ['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount',
                       'urlcount', 'mentioncount']
    x = dataframe[['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'urlcount',
              'mentioncount']]
    # convert strings from data into ints
    for item in fieldnames_list:
        x[item] = pd.to_numeric(x[item], errors='coerce')
    # Replace NaNs with 0s for use in ML
    x = x.replace(np.nan, 0, regex=True)
    y = dataframe['label']
    # Convert labels to a list, then convert labels into ints
    # Bots = 0, Genuine = 1
    y_int = y.values.tolist()
    y_int = [int(0) if x == 'bot' else int(1) for x in y_int]
    y_df = pd.DataFrame(y_int)

    return x, y_df

#This cleans the data we get from twitter for numerical analysis.
def clean_twitter_data_strings_to_ints(dataframe):
    dataframe.fillna(0, inplace=True)
    fieldnames_list = ['favoritecount', 'quotecount', 'replycount', 'retweetcount']
    x = dataframe[['favoritecount', 'quotecount', 'replycount', 'retweetcount']]
    # convert strings from data into ints
    for item in fieldnames_list:
        x[item] = pd.to_numeric(x[item], errors='coerce')
    # Replace NaNs with 0s for use in ML
    x = x.replace(np.nan, 0, regex=True)
    x = x.rename(columns={'favoritecount': 'likecount'})
    return x

def clean_twitter_data_text_analysis(dataframe):
    dataframe.fillna(0, inplace=True)
    fieldnames_list = ['text']
    x = dataframe['text']
    x = x.replace(np.nan, 0, regex=True)
    return x


# Create your models here.
'''
EXAMPLE FOR NEW DJANGO PEOPLE: THIS DID NOT WORK OUT BECAUSE CLASSES RUN AT STARTUP
FUNCTIONS ARE BETTER TO WRITE FOR ML MODELS, AS THEY WONT ALWAYS BE CALLED
class GaussianNB():
    data = read_mongo_data()
    x, y_df = clean_data_strings_to_ints(data)
    x_train, x_test, y_train, y_test = train_test_split(x, y_df, test_size=.35, random_state=0)
    # call and fit model
    model = GaussianNB()
    model = model.fit(x_train, y_train.values.ravel())
    # Make Predictions from split test data, print and heat-map confusion matrix for results
    y_predict = model.predict(x_test)
    #Confusion Matrix does not work in Django rn
    #confusion_matrix = pd.crosstab(y_test, y_predict, rownames=['Actual'], colnames=['Predicted'])
    #print(confusion_matrix)
    #matrix = sb.heatmap(confusion_matrix, annot=True)
    print('Accuracy: ', metrics.accuracy_score(y_test, y_predict))
'''
#helper function to load a model (mfn = Model File Name)
def LoadModel(mfn):
    if mfn == 'gaussianNB':
        model = load('tat/mlModels/gaussianNB.joblib')
    elif mfn == 'LSTMText':
        model = load('tat/mlModels/LSTMModel.joblib')
    return model

#Function for Gaussian-based Naive Bayes numerical analysis
def GaussianNB(db, collect):
    #Load requested data from database
    data = read_mongo_data(db, collect)
    data = clean_twitter_data_strings_to_ints(data)
    x = data.values.tolist()
    #load our model and predict on our new data
    m = LoadModel('gaussianNB')
    predictions = m.predict(x)
    print(predictions)
    #Light number crunching for report
    bot_num = np.sum(predictions=='bot')
    percent = bot_num/len(predictions)*100
    statement = "Out of {} analyzed tweets, {} are suspected bots. That is {}%!".format(len(predictions), bot_num, round(percent,2))
    print(statement)
    return statement

#Function for our LSTM Textual Classifier
def LSTMTextClassifier(db, collect):
    #Load requested data from database
    data = read_mongo_data(db, collect)
    data = clean_twitter_data_text_analysis(data)
    x = data.values.tolist()
    #load model and predict
    '''
    m = LoadModel('LSTMText')
    predictions - m.predict(x)
    '''
    #load model and weights, then open them and predict on new data
    model = 'mlModels/LSTMModel.json'
    weights = 'mlModel/LStmwiegelts_mobilenet.h5'
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        with open(model, 'r') as f:
            model = model_from_json(f.read())
        model.load_weights(weights)
    predictions = model.predict(x)
    statement = "Out of {} analyzed tweets, {} are suspected bots. That is {}%!".format(len(predictions), bot_num, round(percent, 2))
    print(statement)
    return statement

