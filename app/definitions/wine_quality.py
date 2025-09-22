"""
Modeling wine preferences by data mining from physicochemical properties.
Original: https://github.com/Gcav66/learn-dagster-mlflow
Dataset: http://archive.ics.uci.edu/ml/datasets/Wine+Quality
"""

import logging

import dagster as dg
import pandas as pd
import mlflow
import mlflow.sklearn

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

from app.definitions import typedefs as td

DATASETS_BASE_URI = "http://archive.ics.uci.edu/ml/machine-learning-databases"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dg.asset
def wine_quality(wine_dataset):
    np.random.seed(40)
    model_name = "ElasticnetWineModel"
    params = {'alpha': 0.9, 'l1_ratio': 1.0, 'random_state': 42}
    train_x, test_x, train_y, test_y = _load_train_test_data(wine_dataset, col='quality')

    with mlflow.start_run():
        lr_model = ElasticNet(**params).fit(train_x, train_y)
        predictions = lr_model.predict(test_x)
        metrics = _eval_wine_metrics(actual=test_y, pred=predictions)
        logger.info(f"{model_name} - params: {params}, metrics: {metrics}")

        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(  # type: ignore
            sk_model=lr_model,
            artifact_path="sk_models",
            registered_model_name=model_name
        )

    logger.info(f"{model_name} - training complete")


@dg.asset
def wine_dataset() -> pd.DataFrame:
    """Dagster asset with fixed dataset path."""
    return _load_wine_dataset("wine-quality/winequality-red.csv")


def _load_wine_dataset(filepath: str) -> pd.DataFrame:
    return pd.read_csv(f"{DATASETS_BASE_URI}/{filepath}", sep=";")


def _load_train_test_data(data: pd.DataFrame, col: str) -> td.TrainTestTuple:
    train, test = train_test_split(data)
    train_x = train.drop([col], axis=1)
    test_x = test.drop([col], axis=1)
    train_y = train[[col]]
    test_y = test[[col]]
    return train_x, test_x, train_y, test_y


def _eval_wine_metrics(actual: pd.DataFrame, pred: np.ndarray) -> dict[str, float]:
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return {'RMSE': rmse, 'MAE': mae, 'R2': r2}
