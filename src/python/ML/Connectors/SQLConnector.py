from collections import Counter
from random import shuffle

import mysql.connector

from ML.Connectors import Connector


class SQLConnector(Connector):
    def __init__(self, **kwargs):
        self.connection = mysql.connector.connect(**kwargs)
        self.cursor = self.connection.cursor()
    
    def retrieve(self, table, fields, test_size=None, train_size=None, batch_size=None):
        if not batch_size:
            userid_query = f"SELECT userid FROM {table}"
            self.cursor.execute(userid_query)
            userids = Counter(userid for (userid,) in self.cursor)
            
            if test_size is None and train_size is None:
                test_size = 0.25
                train_size = 1 - test_size
            elif train_size is None:
                train_size = 1 - test_size
            elif test_size is None:
                test_size = 1 - train_size
            else:
                raise ValueError('Test and train sizes must be floats that add to 1.')

            num_tweets = sum(userids.values())
            proportions = [(userid, count / num_tweets) for (userid, count) in userids.items()]
            shuffle(proportions)

            train_users = []
            train_total = 0
            for (userid, proportion) in proportions:
                if train_total < train_size:
                    train_users.append(userid)
                    train_total = train_total + proportion

            tweet_query = f"SELECT {', '.join(['userid', *fields])} FROM {table}"
            self.cursor.execute(tweet_query)

            train_set = []
            test_set = []
            for result in self.cursor:
                userid = result[0]
                if userid in train_users:
                    train_set.append(result[1:])
                else:
                    test_set.append(result[1:])

            return train_set, test_set
