import requests

import dagster as dg
import numpy as np
import pandas as pd
import xgboost as xg

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

HACKER_NEWS_URI = "https://hacker-news.firebaseio.com/v0"


@dg.asset
def hackernews_stories():
    """Latest 1000 Hacker News stories"""
    items = _get_latest_hacker_news_items(limit=1000)
    df = pd.DataFrame(items)
    if df.empty:
        return df

    df = df[df.type == "story"]
    return df[~df.title.isna()]


@dg.asset
def latest_story_comment_predictions(xgboost_comments_model, tfidf_vectorizer):
    """Latest 100 Hacker News stories and their predicted comment counts"""
    items = _get_latest_hacker_news_items(limit=100)
    df = pd.DataFrame(items)
    if df.empty:
        return df

    df = df[df.type == "story"]
    df = df[~df.title.isna()]
    inference_x = df.title
    inference_x = tfidf_vectorizer.transform(inference_x)
    return xgboost_comments_model.predict(inference_x)


@dg.multi_asset(outs={
    "training_data": dg.AssetOut(),
    "test_data": dg.AssetOut()
})
def training_test_data(hackernews_stories):
    """Split the dataset to reserve 20% of records as the test set"""
    x = hackernews_stories.title
    y = hackernews_stories.descendants
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    return (x_train, y_train), (x_test, y_test)


@dg.multi_asset(outs={
    "tfidf_vectorizer": dg.AssetOut(),
    "transformed_training_data": dg.AssetOut()
})
def transformed_train_data(training_data):
    """Initiate and fit tokenizer on training data and transform the training dataset"""
    x_train, y_train = training_data
    vectorizer = TfidfVectorizer()
    transformed_x_train = vectorizer.fit_transform(x_train)
    transformed_x_train = transformed_x_train.todense()
    y_train = y_train.fillna(0)
    transformed_y_train = np.array(y_train)
    return vectorizer, (transformed_x_train, transformed_y_train)


@dg.asset
def transformed_test_data(test_data, tfidf_vectorizer):
    """Use the fitted tokenizer to transform the test dataset"""
    X_test, y_test = test_data
    transformed_x_test = tfidf_vectorizer.transform(X_test)
    y_test = y_test.fillna(0)
    transformed_y_test = np.array(y_test)
    return transformed_x_test, transformed_y_test


@dg.asset
def xgboost_comments_model(transformed_training_data):
    """Train highly efficient and flexible XGBoost model"""
    xgb_r = xg.XGBRegressor(
        objective="reg:squarederror",
        eval_metric=mean_absolute_error,
        n_estimators=20
    )
    transformed_x_train, transformed_y_train = transformed_training_data
    xgb_r.fit(transformed_x_train, transformed_y_train)
    return xgb_r


@dg.asset
def comments_model_test_set_r_squared(transformed_test_data, xgboost_comments_model):
    """Use the test set data to get a score of the XGBoost model"""
    transformed_x_test, transformed_y_test = transformed_test_data
    score = xgboost_comments_model.score(transformed_x_test, transformed_y_test)
    return score


def _get_hacker_news_max_item_id():
    response = requests.get(f"{HACKER_NEWS_URI}/maxitem.json")
    response.raise_for_status()
    return response.json()


def _get_hacker_news_item(item_id):
    response = requests.get(f"{HACKER_NEWS_URI}/item/{item_id}.json")
    response.raise_for_status()
    return response.json()


def _get_latest_hacker_news_items(limit=1000):
    latest_id = _get_hacker_news_max_item_id()
    scope = range(latest_id - limit, latest_id)
    return [_get_hacker_news_item(item_id) for item_id in scope]
