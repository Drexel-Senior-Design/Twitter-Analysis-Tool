from collections import Counter
import csv
from pathlib import Path
from random import shuffle

from ML.Connectors import Connector


class FileConnector(Connector):
    def __init__(self, filepath, userkey="userid", fieldnames=None, restkey=None,
            restval=None, dialect='excel', *reader_args, **reader_kwargs):
        self.path = Path(filepath)
        if not self.path.is_file():
            raise ValueError(f"{filepath} does not exist or is not a file")
        self.file = self.path.open(newline='')
        self.userkey = userkey
        self.fieldnames = fieldnames
        self.restkey = restkey
        self.restval = restval
        self.dialect = dialect
        self.reader_args = reader_args
        self.reader_kwargs = reader_kwargs

    def __del__(self):
        self.file.close()

    def make_reader(self):
        return csv.DictReader(
                self.file, self.fieldnames, self.restkey, self.restval,
                self.dialect, *(self.reader_args), **(self.reader_kwargs)
        )

    def reset(self):
        self.file.seek(0)
    
    def retrieve(self, fields, test_size=None, train_size=None, batch_size=None):
        if not batch_size:
            reader = self.make_reader()
            try:
                userids = Counter(row[self.userkey] for row in reader)
            except Exception as e:
                raise
            finally:
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
            train_total = 0
            for (userid, proportion) in proportions:
                if train_total < train_size:
                    train_users.append(userid)
                    train_total = train_total + proportion

            reader = self.make_reader()
            results = ([row[self.userkey], *(row[field] for field in fields)] for row in reader)

            train_set = []
            test_set = []
            try:
                for result in results:
                    userid = result[0]
                    if userid in train_users:
                        train_set.append(result[1:])
                    else:
                        test_set.append(result[1:])
            except Exception as e:
                raise
            finally:
                self.reset()

            return train_set, test_set
