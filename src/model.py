# coding=utf8
from config import *
import pandas as pd
import xgboost as xgb
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np
import sys


def fair_obj(preds, dtrain):
    fair_constant = 2
    labels = dtrain.get_label()
    x = (preds - labels)
    den = abs(x) + fair_constant
    grad = fair_constant * x / (den)
    hess = fair_constant * fair_constant / (den * den)
    return grad, hess


def train():
    dataset = pd.read_csv(FEATURE_FILE, header=None)
    X = dataset.drop([0, len(dataset.columns) - 1], axis=1)
    y = dataset[len(dataset.columns) - 1]
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2)

    dtrain = xgb.DMatrix(train_X, label=train_y)
    dtest = xgb.DMatrix(test_X)
    params = {'eta': 0.03, 'seed': 0, 'subsample': 0.8, 'colsample_bytree': 0.8, 'max_depth': 8,
              'min_child_weight': 1, 'silent': 0, 'eval_metric': 'mae', }
    watchlist = [(dtrain, 'train')]
    bst = xgb.train(params, dtrain, num_boost_round=2000, evals=watchlist, obj=fair_obj)
    pred_y = bst.predict(dtest)
    print metrics.mean_absolute_error(test_y, pred_y)
    """
    print test result
    """
    """
    Y = test_y.tolist()
    test_x = np.array(test_X).tolist()
    for index, py in enumerate(pred_y.tolist()):
        print test_x[index], Y[index], py
    """
    return bst

def predict(bst):
    dataset = pd.read_csv(REAL_TEST_FILE, header=None)
    X = dataset.drop([0], axis=1)
    users = dataset[0]
    pred_y = bst.predict(xgb.DMatrix(X))
    with open('./submit.csv', 'w') as out:
        out.write('user_id,user_gmv\n')
        for index, y in enumerate(pred_y.tolist()):
            if y < 1.0:
                y = 1.0
            if y < 0.0:
                y = 0.0
            out.write('%s,%f\n' % (users[index], y))


if __name__ == "__main__":
    model = "train1"
    if model == "train":
        train()
    else:
        bst = train()
        predict(bst)
