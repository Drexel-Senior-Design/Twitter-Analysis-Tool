from ML.Connectors import Connector

class MockConnector(Connector):
    def retrieve(self):
        return [1, 2, 3, 4, 5]
    def train_test_split(self):
        return [1, 2, 3, 4], [5]
