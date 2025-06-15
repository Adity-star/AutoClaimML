# 🚗 Vehicle Data Pipeline Project

This project is an end-to-end ML pipeline integrating **MongoDB**, **AWS (S3, EC2, IAM, ECR)**, **Docker**,**DVC**,**Mlflow**, **CI/CD with GitHub Actions**, and **FastAPI/Flask app** deployment. It automates data ingestion, validation, transformation, model training, evaluation, and deployment using robust engineering practices.

![image](https://github.com/user-attachments/assets/3e1a92d3-d9de-4eda-b49c-a0e66fcdb0b5)


---

## 🛠️ Project Setup Instructions

### 1. Project Initialization

- Run the following script to create the project structure:

```bash
python template.py
```
- Update setup.py and pyproject.toml to support local package imports.

2. Virtual Environment
```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
pip list  # Confirm all packages are installed

```
## 🗄️ MongoDB Atlas Setup  
- Create an account at MongoDB Atlas.
- Create a new project > cluster (M0) > setup DB user.
- Set Network Access to 0.0.0.0/0 to allow public access.
- Get the Python driver connection string and save it (replace <password>).
- Create a folder notebook/ and add your dataset + mongoDB_demo.ipynb.
- Use the notebook to push your data to MongoDB.
- Verify data in: MongoDB Atlas → Database → Browse Collections.

# 🔧 Logging, Exception, and EDA

- Implement and test `logger.py` and `exception.py` using `demo.py`.
- Add EDA and Feature Engineering notebooks inside `notebook/`.

---

# 📥 Data Ingestion Pipeline

### 1. Configuration Setup

- Declare config variables in `constants/__init__.py`.
- Setup MongoDB connection in `configuration/mongo_db_connections.py`.
- Connect MongoDB using `data_access/proj1_data.py`.

### 2. Define Configuration Classes

- `entity/config_entity.py`: `DataIngestionConfig`
- `entity/artifact_entity.py`: `DataIngestionArtifact`

### 3. Data Ingestion Logic

- Build the ingestion logic in `components/data_ingestion.py`.
- Run `demo.py` after setting the `MONGODB_URL` in your environment.


### 4. Set Environment Variables

#### Bash
```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster..."
```
---

# 🔄 Data Validation, Transformation & Model Training

- Update `utils/main_utils.py` and `config/schema.yaml` for validation.

- Build the following components similar to data ingestion:

  - **Data Validation**

  - **Data Transformation** (include `estimator.py`)

  - **Model Training** (extend `estimator.py`)
  ---
  
## 📊 Experiment & Data Versioning with DVC and MLflow
### DVC (Data Version Control)
- Track datasets, models, and pipeline outputs with DVC to ensure reproducibility.
- Initialize DVC:
```bash
dvc init
dvc remote add -d storage s3://my-dvc-storage-bucket/path
```
- Track files and push to remote:
```
dvc add data/raw_dataset.csv
dvc add models/model.pkl
git add data/.gitignore *.dvc
git commit -m "Track dataset and model artifacts with DVC"
dvc push
```
- Define pipeline stages in dvc.yaml to automate workflow:
- Run the pipeline:

```bash
dvc repro
dvc push
```
## MLflow Tracking
- Log experiments, parameters, metrics, and artifacts with MLflow.
- Example usage inside `components/model_trainer.py`
- Use MLflow UI to track and compare your runs.

 
  ---
 
# ☁️ AWS Setup for Model Registry
  

## IAM User Setup

- Create user: `firstproj`
- Attach policy: `AdministratorAccess`
- Download credentials (CSV)

---

## Set Environment Variables

### Bash
```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### Configure Project Files
Add credentials to `constants/__init__.py`:
```python
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "my-model-mlopsproj"
MODEL_PUSHER_S3_KEY = "model-registry"
```
- Implement:

- `src/configuration/aws_connection.py`
- `src/aws_storage/`
- `entity/s3_estimator.py`

### S3 Setup:
- Create bucket: my-model-mlopsproj
- Region: us-east-1
- Uncheck "Block all public access"

---
# ✅ Model Evaluation & Model Pusher

- Build components for model evaluation and model pusher.

- These use previously built logic to compare and push models to S3.

# Prediction Pipeline

- Setup `app.py` and the routing logic.

- Add directories:
  - `static/`
  - `templates/`

# CI/CD Pipeline with GitHub Actions + Docker + EC2

## 1. Docker Setup
- Create `Dockerfile` and `.dockerignore`

## 2. GitHub Actions
- Path: `.github/workflows/aws.yaml`

## 3. AWS Resources
- IAM User: `usvisa-user`
- ECR Repo: `vehicleproj`
- EC2 Ubuntu Server:
  - AMI: Ubuntu 24.04
  - Type: t2.medium
  - Key Pair: `proj1key`
  - Storage: 30GB
  - Allow HTTP/HTTPS
  - Name: `vehicledata-machine`

## 4. EC2 Docker Installation

```bash
sudo apt-get update -y
sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

## 5. Self-Hosted GitHub Runner on EC2

- Go to GitHub → Settings → Actions → Runner → Add Linux Runner
- Run all `./config.sh` and `./run.sh` commands on EC2
- Confirm status = **idle** on GitHub

---

## 6. GitHub Secrets

| Secret Key             | Description                     |
|-----------------------|---------------------------------|
| `AWS_ACCESS_KEY_ID`     | Your AWS IAM Access Key          |
| `AWS_SECRET_ACCESS_KEY` | Your AWS IAM Secret Access Key   |
| `AWS_DEFAULT_REGION`    | `us-east-1`                     |
| `ECR_REPO`              | Your ECR repo URI                |

## 7. Expose Port 5080 for Web App

- EC2 → Security Groups → Edit Inbound Rules:
  - Type: Custom TCP
  - Port: 5080
  - Source: 0.0.0.0/0

---

## 8. Launch App

Access your app from browser using:

```cpp
http://<your-ec2-public-ip>:5080
```
## Author & Acknowledgments
Developed with ❤️ for full-lifecycle MLOps deployment.
Contributions, improvements, and suggestions are welcome!

## 📄 License
This project is licensed under the [MIT License.](https://github.com/Adity-star/AutoClaimML#)
