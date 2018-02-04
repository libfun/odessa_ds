from flask import Flask, request, abort
from flask.json import dumps
import json
import logging
import os
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, \
    GradientBoostingClassifier
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s]:%(name)s%(levelname)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
if not os.path.exists('./log'):
    os.mkdir('./log')
fh = logging.FileHandler('./log/predict.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


class Data(object):
    def __init__(self):
        self.mean_age = 0

    def __call__(self, X, y=None, train=True):
        X = X[['Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Pclass']]
        X['Sex'] = (X.Sex == 'male').values.astype('int')
        ohe_embarked = pd.get_dummies(X['Embarked'], prefix='embarked')
        X = X.drop('Embarked', axis=1)
        X = pd.concat([X, ohe_embarked], axis=1)

        ohe_pclass = pd.get_dummies(X['Pclass'], prefix='pclass')
        X = X.drop('Pclass', axis=1)
        X = pd.concat([X, ohe_pclass], axis=1)

        if train:
            self.mean_age = X.Age.mean()

        X.loc[X.Age.isna(), 'Age'] = self.mean_age

        print(X)

        # X.columns = ['Sex', 'Age', 'SibSp', 'Parch', 'Fare',
        #              'embarked_C', 'embarked_Q', 'embarked_S',
        #              'pclass_1', 'pclass_2', 'pclass_3']

        df =  pd.DataFrame(columns=['Sex', 'Age', 'SibSp', 'Parch', 'Fare',
                     'embarked_C', 'embarked_Q', 'embarked_S',
                     'pclass_1', 'pclass_2', 'pclass_3'])
        df = df.append(X, ignore_index=True)
        df = df.fillna(0)

        return df.values, y


@app.route('/script', methods=['POST'])
def respond():
    print(request.args)
    df = pd.DataFrame(columns=['PassengerId', 'Pclass',
                               'Name', 'Sex', 'Age', 'SibSp',
                               'Parch', 'Ticket', 'Fare', 'Cabin',
                               'Embarked'])
    input_data = request.get_json()
    for i in input_data['data']:
        print(i)
        df = df.append(dict(i), ignore_index=True)
    print(df)

    # ndf = df.drop(['PassengerId'])
    data_transform = Data()
    data_transform.mean_age = 29.69911764705882
    X, _ = data_transform(df)

    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)

    result = clf.predict_proba(X)

    return dumps({"result": result.tolist()})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6007)
