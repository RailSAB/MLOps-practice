# MLOps Practice

This project demonstrates a full **MLOps pipeline** for a machine learning model:  
from data preprocessing → model training → deployment of API and frontend via Docker.  

**Focus**: The project emphasizes pipeline automation and orchestration, featuring:
- Simple frontend interface
- Basic logistic regression model 
- Binary classification task
- Dataset: [Airline Passenger Satisfaction from Kaggle](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction/data?select=train.csv)

---

## 🔹 Project Structure

```
├── code
│ ├── datasets
│ ├── deployment # Docker + services
│ │ ├── api # FastAPI backend
│ │ └── app # Streamlit frontend
│ └── models # training scripts
├── data
│ ├── raw # raw input data
│ └── processed # processed datasets
├── models # saved models and scalers (pkl)
├── services
│ └── airflow
│ ├── dags # Airflow DAGs
│ └── logs # Airflow logs
└── requirements.txt # dependencies
```

---

## 🔹 Tech Stack

- **Airflow** — pipeline orchestration (0.0.0.0:8080)  
- **MLflow** — experiment tracking (127.0.0.1:5000)  
- **FastAPI** — REST API for serving the model (localhost:8000)  
- **Streamlit** — frontend for interaction (localhost:8501)  
- **Docker Compose** — deployment of API & frontend services  

---

## 🔹 Setup & Run

### 1. Create virtual environments
Set up a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
export AIRFLOW_HOME=$(pwd)/services/airflow

pip install -r requirements.txt
```

📦 requirements.txt includes:

```
apache-airflow
pandas
numpy
scikit-learn
mlflow-skinny
```

⚠️ For MLflow, it's recommended to use a separate environment, since it can cause conflicts with apache-airflow:

```bash
pip install mlflow
```

### 2. Run services

#### Airflow
```bash
airflow standalone
```
Web UI available at: http://0.0.0.0:8080

Username/password will be shown in the terminal on first startup, or you can find credentials in MLOps-practice/services/airflow/simple_auth_manager_passwords.json.generated

#### MLflow
In a separate environment:

```bash
mlflow ui
```
UI available at: http://127.0.0.1:5000

#### Docker
Install Docker and verify it's running:

```bash
docker --version
```

### 3. Airflow DAGs
DAGs are located in services/airflow/dags.
There are two ways to run pipelines:

**Step by step**

- data_pipeline_dag — data cleaning & encoding
- model_training_dag_simple — model training
- deploy_model_pipeline — Docker deployment

**Full pipeline**

- full_pipeline_dag — runs the entire flow (data → training → deploy)
- scheduled to run every 5 minutes

---

## 🔹 Pipeline Logic

### Data pipeline

- drop NaN values
- label & one-hot encoding
- save results in data/processed/

### Model training

- scale data
- train logistic regression (GridSearchCV)
- log metrics into MLflow
- save best model & scaler into models/

### Deployment

- build Docker images for FastAPI & Streamlit
- start containers:
  - API: http://localhost:8000
  - App: http://localhost:8501

---

## 🔹 Experiment Tracking
Open MLflow UI: http://127.0.0.1:5000
Here you can monitor:

- metrics (accuracy, precision, recall, f1)
- trained models

---

## 🔹 Automatic Scheduling
full_pipeline_dag is configured with cron `*/5 * * * *` → runs every 5 minutes.
The pipeline executes in sequence:

1. prepare data
2. train model
3. deploy services