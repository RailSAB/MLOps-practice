import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Customer_Satisfaction_Experiment")

data_train = pd.read_csv(DATA_DIR / "train_processed.csv")
data_test = pd.read_csv(DATA_DIR / "test_processed.csv")

X_test = data_test.drop("satisfaction", axis=1)
y_test = data_test["satisfaction"]
X = data_train.drop("satisfaction", axis=1)
y = data_train["satisfaction"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

logreg_params = {"penalty": ["l1", "l2", "elasticnet", "none"]}
logreg = LogisticRegression(max_iter=1000, solver="saga") 
logreg_grid = GridSearchCV(logreg, logreg_params, cv=5, scoring="accuracy")

with mlflow.start_run():
    logreg_grid.fit(X_train_scaled, y_train)
    logreg_best = logreg_grid.best_estimator_

    y_pred_logreg = logreg_best.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred_logreg)
    precision = precision_score(y_test, y_pred_logreg)
    recall = recall_score(y_test, y_pred_logreg)
    f1 = f1_score(y_test, y_pred_logreg)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)

    mlflow.sklearn.log_model(logreg_best, "logreg_best")
    joblib.dump(logreg_best, MODEL_DIR / "logreg_best3.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

