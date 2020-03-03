"""
Adapters for different machine learning frameworks' models to be used
with MLFlow training process. Currently only supports Sklearn.
"""
from abc import ABC, abstractmethod

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from .sklearn_models import SklearnModel, SklearnGridSearchCV


class BaseModel(ABC):
    """
    Abstract base class for models to be trained with MLFlow
    """

    @abstractmethod
    def fit(self, X, y):
        """
        Fit the model
        """

    @abstractmethod
    def predict(self, X):
        """
        Return inference results
        """

    @abstractmethod
    def score(self, X, y):
        """
        Scores the model against provided X, y
        """

    @abstractmethod
    def scores(self, X, y, scoring, cv=5):
        """
        Cross val score the model and return scoring results
        """

    @abstractmethod
    def save(self, artifact_path):
        """
        Save the model to specified artifact path.
        """

    @staticmethod
    @abstractmethod
    def load(uri, name):
        """
        Load a model from the specified uri
        """


ALL_MODELS = [
    SklearnModel(model=GaussianNB()),
    SklearnModel(model=KNeighborsClassifier()),
    SklearnModel(model=AdaBoostClassifier()),
    SklearnModel(model=RandomForestClassifier()),
    SklearnGridSearchCV(
        model=KNeighborsClassifier(),
        param_grid={"n_neighbors": range(2, 10)},
        name="GridSearchKNeighbors",
    ),
    SklearnGridSearchCV(
        model=RandomForestClassifier(),
        param_grid={"n_estimators": [5, 10, 100, 200, 500]},
        name="GridSearchRandomForest",
    ),
    SklearnGridSearchCV(
        model=AdaBoostClassifier(),
        param_grid={
            "n_estimators": [20, 50, 100, 200],
            "learning_rate": [0.1, 0.5, 0.75, 1],
        },
        name="GridSearchAdaBoost",
    ),
]
