from collections import Counter
from random import shuffle

import pandas as pd
import sqlalchemy

from ML.Connectors import Connector


class SQLConnector(Connector):
    def __init__(self, user, password, location, database):
        self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{location}/{database}')
   
    def retrieve(self, table, fields):
        return pd.read_sql(table, self.engine, columns=fields)

    def train_test_split(self, table, fields, test_size=None, train_size=None):
        with self.engine.connect() as connection:
            userid_query = f"SELECT userid FROM {table}"
            result = connection.execute(userid_query)
            userids = Counter(userid for (userid,) in result)
            
            if test_size is None and train_size is None:
                test_size = 0.25
                train_size = 1 - test_size
            elif train_size is None:
                train_size = 1 - test_size
            elif test_size is None:
                test_size = 1 - train_size
            elif train_size + test_size != 1:
                raise ValueError('Test and train sizes must be floats that add to 1.')

            num_tweets = sum(userids.values())
            proportions = [(userid, count / num_tweets) for (userid, count) in userids.items()]
            shuffle(proportions)

            train_users = []
            test_users = []
            train_total = 0
            for (userid, proportion) in proportions:
                if train_total < train_size:
                    train_users.append(userid)
                    train_total = train_total + proportion
                else:
                    test_users.append(userid)

            tweets = pd.read_sql(table, connection, columns=['userid', *fields])

            train_set = tweets.loc[tweets["userid"].isin(train_users)]
            test_set = tweets.loc[tweets["userid"].isin(test_users)]

            return train_set, test_set
