from pendulum import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_TRAIN_DATA_PATH = RAW_DIR / "train.csv"
RAW_TEST_DATA_PATH = RAW_DIR / "test.csv"
PREPROCESSED_TRAIN_DATA_PATH = PROCESSED_DIR / "train_processed.csv"
PREPROCESSED_TEST_DATA_PATH = PROCESSED_DIR / "test_processed.csv"

def remove_nan():
    data_train = pd.read_csv(RAW_TRAIN_DATA_PATH)
    data_test = pd.read_csv(RAW_TEST_DATA_PATH)

    data_train.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)
    data_test.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)

    mean_arrival_delay = data_train['Arrival Delay in Minutes'].mean()
    data_train['Arrival Delay in Minutes'] = data_train['Arrival Delay in Minutes'].fillna(mean_arrival_delay)
    data_test['Arrival Delay in Minutes'] = data_test['Arrival Delay in Minutes'].fillna(mean_arrival_delay)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    train_path = PROCESSED_DIR / "train_no_nan.csv"
    test_path = PROCESSED_DIR / "test_no_nan.csv"
    data_train.to_csv(train_path, index=False)
    data_test.to_csv(test_path, index=False)

    return str(train_path), str(test_path)


def encode_features(**context):
    ti = context['ti']
    train_path, test_path = ti.xcom_pull(task_ids='remove_nan')

    data_train = pd.read_csv(train_path)
    data_test = pd.read_csv(test_path)

    le = LabelEncoder()
    data_train['satisfaction'] = le.fit_transform(data_train['satisfaction'])
    data_test['satisfaction'] = le.transform(data_test['satisfaction'])

    cat_col = data_train.select_dtypes(include=['object']).columns
    encoder = OneHotEncoder(drop='first')
    encoder.fit(data_train[cat_col])

    train_encoded = encoder.transform(data_train[cat_col])
    test_encoded = encoder.transform(data_test[cat_col])

    train_encoded_df = pd.DataFrame(train_encoded.toarray(), columns=encoder.get_feature_names_out(cat_col), index=data_train.index)
    test_encoded_df = pd.DataFrame(test_encoded.toarray(), columns=encoder.get_feature_names_out(cat_col), index=data_test.index)

    data_train_encoded = pd.concat([data_train.drop(cat_col, axis=1), train_encoded_df], axis=1)
    data_test_encoded = pd.concat([data_test.drop(cat_col, axis=1), test_encoded_df], axis=1)

    data_train_encoded.to_csv(PREPROCESSED_TRAIN_DATA_PATH, index=False)
    data_test_encoded.to_csv(PREPROCESSED_TEST_DATA_PATH, index=False)

with DAG(
    dag_id="data_pipeline_dag",
    start_date=datetime(2025, 9, 14, hour=14, tz="Europe/Moscow"),
    schedule=None,
    catchup=False) as dag:

    task_load_clean = PythonOperator(
        task_id="remove_nan", 
        python_callable=remove_nan
    )

    task_encode = PythonOperator(
        task_id="encode_features", 
        python_callable=encode_features
    )

    task_load_clean >> task_encode
