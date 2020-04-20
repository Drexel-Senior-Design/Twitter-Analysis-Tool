from collections import Counter
import csv
from pathlib import Path
from random import shuffle

import pandas as pd

from ML.Connectors import Connector


class FileConnector(Connector):
    def __init__(self, filepath):
        self.path = Path(filepath)
        if not self.path.is_file():
            raise ValueError(f"{filepath} does not exist or is not a file")
        self.file = self.path.open(newline='')

    def __del__(self):
        self.file.close()

    def reset(self):
        self.file.seek(0)

    def retrieve(self, fields, dtype):
        tweets = pd.read_csv(self.file, usecols=fields, dtype=dtype)
        self.reset()
        return tweets
    
    def train_test_split(self, fields, dtype, test_size=None, train_size=None):
        reader = csv.DictReader(self.file)
        userids = Counter(row['userid'] for row in reader)
        self.reset()

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
        test_users = []
        train_total = 0
        for (userid, proportion) in proportions:
            if train_total < train_size:
                train_users.append(userid)
                train_total = train_total + proportion
            else:
                test_users.append(userid)

        tweets = pd.read_csv(self.file, usecols=['userid', *fields], dtype={'userid': str, **dtype})

        train_set = tweets.loc[tweets['userid'].isin(train_users)]
        test_set = tweets.loc[tweets['userid'].isin(test_users)]
        
        self.reset()

        return train_set, test_set
