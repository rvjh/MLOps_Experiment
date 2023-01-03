
import pandas as pd
import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

import mlflow
from prefect import flow,task
from prefect.task_runners import ConcurrentTaskRunner

@task
def read_dataframe(filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)

        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    elif filename.endswith('.parquet'):
        df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    return df
@task
def add_features(df_train,df_val):
    #df_train = read_dataframe(train_path)
    #df_val = read_dataframe(val_path)

    print(f"Training length : {len(df_train)}"),
    print(f"Validation length : {len(df_val)}")
    df_train['PU_DO'] = df_train['PULocationID'] + '_' + df_train['DOLocationID']
    df_val['PU_DO'] = df_val['PULocationID'] + '_' + df_val['DOLocationID']

    categorical = ['PU_DO'] #'PULocationID', 'DOLocationID']
    numerical = ['trip_distance']
    dv = DictVectorizer()

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    val_dicts = df_val[categorical + numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts)

    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    return X_train,X_val,y_train,y_val,dv

#### Modeling Section#####

import xgboost as xgb

## Hyperopt function for finding the best parameter
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

@task
def train_model_search(train, valid, y_val):
    def objective(params):
        with mlflow.start_run():
            mlflow.set_tag("model","xgboost")
            mlflow.log_params(params)
            booster = xgb.train(params=params,
                               dtrain=train,
                               num_boost_round=20,                 ## original 1000
                               evals=[(valid,"validation")],
                               early_stopping_rounds=5)            ## original 50
            y_pred = booster.predict(valid)
            rmse = mean_squared_error(y_val,y_pred,squared=False)
            mlflow.log_metric("rmse",rmse)
        return {'loss' : rmse, 'status' : STATUS_OK }

    search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
        'learning_rate': hp.loguniform('learning_rate', -3, 0),
        'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
        'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
        'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
        'objective': 'reg:linear',
        'seed': 42
    }
    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=1,
        trials=Trials()
    )

@task
def train_best_model(train, valid, y_val,dv):
    with mlflow.start_run():
        best_params = {
            'learning_rate': 0.45760137492869973,
            'max_depth': 25,
            'min_child_weight': 1.636092085289727,
            'objective': 'reg:linear',
            'reg_alpha': 0.06801680013571364,
            'reg_lambda': 0.16306576846442025,
            'seed': 42}

        mlflow.log_params(best_params)

        booster = xgb.train(params=best_params,
                            dtrain=train,
                            num_boost_round=20,  ## original 1000
                            evals=[(valid, "validation")],
                            early_stopping_rounds=5)  ## original 50
        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)

        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
@flow(task_runner = ConcurrentTaskRunner())
def main(train_path = './data/green_tripdata_2021-01.parquet',
         val_path = './data/green_tripdata_2021-02.parquet'):
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("nyc-taxi-experiment")

    X_train = read_dataframe(train_path)
    X_val = read_dataframe(val_path)
    X_train,X_val,y_train,y_val,dv = add_features(X_train, X_val).result()
    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_val, label=y_val)
    train_model_search(train, valid, y_val)
    train_best_model(train, valid, y_val,dv)

main()