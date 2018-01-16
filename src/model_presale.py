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


def train(eta=0.03,max_depth=8):
    dataset = pd.read_csv(FEATURE_FILE, header=None)
    X = dataset.drop([0, len(dataset.columns) - 1], axis=1)
    y = dataset[len(dataset.columns) - 1]
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.05)

    dtrain = xgb.DMatrix(train_X, label=train_y)
    dtest = xgb.DMatrix(test_X)
    params = {'eta': eta, 'seed': 0, 'subsample': 0.8, 'colsample_bytree': 0.8, 'max_depth': max_depth,
              'min_child_weight': 1, 'silent': 0, 'eval_metric': 'mae', }
    watchlist = [(dtrain, 'train')]
    bst = xgb.train(params, dtrain, num_boost_round=2000, evals=watchlist, obj=fair_obj)
    pred_y = bst.predict(dtest)
    user_dict = after_predict_2016()
    pred_y_2016 = []
    users = dataset[0]
    for index, y in enumerate(pred_y.tolist()):
        if y < 1.0:
            y = 1.0
        # if users[index] in user_dict and y < user_dict[users[index]]:
        #     y = user_dict[users[index]]
        pred_y_2016.insert(index, y)

    mae = metrics.mean_absolute_error(test_y, pred_y_2016)
    print metrics.mean_absolute_error(test_y, pred_y_2016)
    """
    print test result
    """
    """
    Y = test_y.tolist()
    test_x = np.array(test_X).tolist()
    for index, py in enumerate(pred_y.tolist()):
        print test_x[index], Y[index], py
    """
    return bst, mae,


def after_predict():
    user_dict = {}
    with open(eval("PROMOTION_CONSUMPTION_LAST2YEARS_2017"), 'r') as infile:
        for line in infile:
            items = line.decode('utf8').strip('\r\n').split(',')
            user_dict[items[0]] = user_dict.get(items[0], 0) + float(items[6])
    return user_dict

def after_predict_2016():
    user_dict = {}
    with open(eval("PROMOTION_CONSUMPTION_LAST2YEARS_2016"), 'r') as infile:
        for line in infile:
            items = line.decode('utf8').strip('\r\n').split(',')
            user_dict[items[0]] = user_dict.get(items[0], 0) + float(items[6])
    return user_dict

def predict(bst,eta=0.03,max_depth=8, mae=100):
    dataset = pd.read_csv(REAL_TEST_FILE, header=None)
    X = dataset.drop([0], axis=1)
    users = dataset[0]
    pred_y = bst.predict(xgb.DMatrix(X))
    user_dict = after_predict()
    with open('./submit_' + str(eta) + '_' + str(max_depth) + '_' + str(mae) + '.csv', 'w') as out:
        out.write('user_id,user_gmv\n')
        for index, y in enumerate(pred_y.tolist()):
            if y < 1.0:
                y = 1.0
            if users[index] in user_dict and y < user_dict[users[index]]:
                y = user_dict[users[index]]
            out.write('%s,%f\n' % (users[index], y))


if __name__ == "__main__":

    for eta in [0.02]:
        for max_depth in [7]:
            bst, mae = train(eta, max_depth)
            predict(bst, eta, max_depth, mae)

