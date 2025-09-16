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

from app.definitions import typedefs

ALPHA = 0.9
L1_RATIO = 1.0
MODEL_NAME = "ElasticnetWineModel"
DATASETS_BASE_URI = "http://archive.ics.uci.edu/ml/machine-learning-databases"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dg.asset
def wine_quality():
    np.random.seed(40)
    params = {'alpha': ALPHA, 'l1_ratio': L1_RATIO}
    data = load_wine_dataset(filepath="wine-quality/winequality-red.csv")
    train_x, test_x, train_y, test_y = _load_train_test_data(data, column='quality')

    with mlflow.start_run():
        lr = ElasticNet(alpha=ALPHA, l1_ratio=L1_RATIO, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)

        rmse, mae, r2 = eval_wine_metrics(test_y, predicted_qualities)
        metrics = {'RMSE': rmse, 'MAE': mae, 'R2': r2}
        logger.info(f"{MODEL_NAME} - params: {params}, metrics: {metrics}")

        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(  # type: ignore
            sk_model=lr,
            artifact_path="sk_models",
            registered_model_name=MODEL_NAME
        )

    logger.info("{MODEL_NAME} - training complete")


@dg.op
def load_wine_dataset(filepath: str) -> pd.DataFrame:
    return pd.read_csv(f"{DATASETS_BASE_URI}/{filepath}", sep=';')


@dg.op
def eval_wine_metrics(
    actual: pd.DataFrame,
    pred: np.ndarray
) -> tuple[float, float, float]:
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def _load_train_test_data(data: pd.DataFrame, column: str) -> typedefs.TrainTestTuple:
    train, test = train_test_split(data)
    train_x = train.drop([column], axis=1)
    test_x = test.drop([column], axis=1)
    train_y = train[[column]]
    test_y = test[[column]]
    return train_x, test_x, train_y, test_y
