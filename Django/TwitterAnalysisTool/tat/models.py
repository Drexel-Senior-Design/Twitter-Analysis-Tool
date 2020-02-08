'''
Rush Weigelt
Feb 2020
This script is to create Django objects out of our ML models
'''

#Django imports
from django.db import models
#ML imports
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import cross_validate, train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
#import seaborn as sb
from sklearn import metrics
from pymongo import MongoClient

#db vars
ourHost = 'bvm15.cci.drexel.edu'
'''
#Defintion for connection to the database
def _connect_mongo(host, port, username, password, db):
    small, reusable function to connect to mongodb
    if username and password:
        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = MongoClient(mongo_uri)
        else:
            conn = MongoClient(host, port)

        print("successfully connected to database")

        return conn[db]

'''

def read_mongo_data():
    client = MongoClient('bvm15.cci.drexel.edu')
    db = client['combined']
    test = db.multi_bot_and_genuine_200k_split
    test = pd.DataFrame(list(test.find()))
    #print(test)
    return test
    #Create query to the specific DB and Collection
    #cursor = db[collection].find(query)
    #print(cursor)
    #Make cursor into DF
    #df = pd.DataFrame(list(cursor))
    #Delete ID col
    #if no_id:
        #del df['_id']
    #return df

# Create your models here.

class GaussianNB():
    data = read_mongo_data()
    data.fillna(0, inplace=True)
    x = data[['followerscount', 'friendscount', 'replycount', 'likecount', 'retweetcount', 'hashtagcount', 'urlcount',
              'mentioncount']]
    y = data['label']
    #bots = 0, genuine = 1
    y = [1 if i!='bot' else 0 for i in y]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.35, random_state=0)
    # call and fit model
    model = GaussianNB()
    model = model.fit(x_train, y_train)
    # Make Predictions from split test data, print and heat-map confusion matrix for results
    y_predict = model.predict(x_test)
    confusion_matrix = pd.crosstab(y_test, y_predict, rownames=['Actual'], colnames=['Predicted'])
    print(confusion_matrix)
    matrix = sb.heatmap(confusion_matrix, annot=True)
    print('Accuracy: ', metrics.accuracy_score(y_test, y_predict))

