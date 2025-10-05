# 🚗 AutoClaimML — Vehicle Insurance Data Pipeline  
### *End-to-End MLOps System for Real-World Claim Automation*

![MLOps](https://img.shields.io/badge/MLOps-End_to_End-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-Deployed-orange?style=flat-square)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?style=flat-square)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue?style=flat-square)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-yellow?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-lightgrey?style=flat-square)

---

## 🧠 Overview

**AutoClaimML** is a full-scale **MLOps project** designed to automate and streamline **vehicle insurance claim processing** using **cloud-integrated pipelines** and **CI/CD automation**.

This project demonstrates a **production-grade ML lifecycle** — from raw data ingestion in **MongoDB Atlas** to **AWS model deployment** — engineered to impress recruiters and simulate real-world enterprise systems.

Whether you’re exploring end-to-end pipelines, CI/CD automation, or real-world ML project architecture, this repository is your go-to reference hub.  

---

## 📂 Project Setup & Structure

```bash
AutoClaimML/
│
├── cloud_storage/           # AWS model storage integration
├── components/              # Core ML components (ingestion, validation, training)
├── configuration/           # Configuration management (MongoDB, AWS, schema)
├── constants/               # Centralized project constants
├── data_access/             # Data ingestion from MongoDB
├── entity/                  # Data entities, estimators, and artifacts
├── exception/               # Custom error handling
├── logger/                  # Logging configuration
├── pipeline/                # Training and prediction pipelines
├── utils/                   # Helper utilities (DVC, validation, etc.)
├── app.py                   # FastAPI/Flask-based prediction service
├── Dockerfile               # Docker container setup
├── .github/workflows/       # CI/CD pipeline for AWS deployment
└── requirements.txt          # Dependencies list
```
---

## Step-by-Step Setup
#### 1. Project Template
Run `template.py` to auto-generate folder structure and boilerplate files.

#### 2.  Virtual Environment & Dependencies
Configure local packages using `setup.py` and `pyproject.toml`.
```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
```

---

## MongoDB Setup & Data Management
#### 3. MongoDB Atlas Configuration
- Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database)
- Whitelist all IPs (`0.0.0.0/0`), and retrieve your connection string.
- set the Environment Variables.
```bash
# Bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/"

# PowerShell
$env:MONGODB_URL = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
```
#### 4. Data Push
-  Use `notebook/mongoDB_demo.ipynb` to push initial dataset to your MongoDB collection and verify in Atlas → Database → Collections.

---
### Logging, EDA & Exception Handling
#### 5. Logging & Exception Setup

Custom logger and unified exception handlers defined in `logger/` and `exception/.`

#### 6. EDA & Feature Engineering

Perform exploratory analysis and feature transformations in notebooks/`EDA_Feature_Engg.ipynb` outputs feed directly into training pipelines.

---
### Data Pipeline Stages
#### 7️. Data Ingestion
- Defined in `configuration.mongo_db_connections.py`
- Fetches and transforms data via `components/data_ingestion.py`
 Configs stored in `entity/config_entity.py` and `entity/artifact_entity.py`

#### 8️. Data Validation
- Schema defined in `config/schema.yaml`
- Validation logic in `utils/main_utils.py` ensures schema integrity before transformation.

#### 9️. Data Transformation

- Core transformation in `components/data_transformation.py`.
- Feature scaling and encoding handled by `entity/estimator.py`.

#### 10. Model Training
- Algorithms implemented in `components/model_trainer.py`
- Reusable estimator architecture for training multiple models.
---
###  AWS Model Deployment & Evaluation
#### 11. AWS Setup
- Create IAM user and S3 bucket (my-model-mlopsproj)
- Configure credentials:
```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET"
```

#### 12️. Model Evaluation & S3 Push
- Evaluate models, push best model to S3 via `entity/s3_estimator.py`
- Retrieval handled automatically during inference.

---

#### 13️. Model Pusher
- Implements model registry logic — updates the production model version.

#### 14️. Prediction Service
- `app.py` exposes a web API (Flask/FastAPI) for real-time predictions.
- Includes templates & static directories for basic web UI.

---
###  CI/CD Automation
### 15️. Docker & GitHub Actions
- Dockerfile + .dockerignore for containerization.
- GitHub Secrets setup for:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`
  - `ECR_REPO`

#### 16️. AWS EC2 + ECR Integration
- EC2 instance configured as GitHub self-hosted runner.
- Docker deployed via GitHub Actions workflow.

#### 17️. Access Deployed App
- Expose port 5080 and access your app at:
```bash
http://<EC2_public_ip>:5080
```

---
### Project Workflow Summary

```mermaid

flowchart LR
    A[MongoDB Data Ingestion] --> B[Data Validation]
    B --> C[Data Transformation]
    C --> D[Model Training]
    D --> E[Model Evaluation]
    E --> F[AWS Model Pusher]
    F --> G[Docker Deployment]
    G --> H[CI/CD with GitHub Actions]
```
---
### Tools and Technologies.

| Category             | Tools                       |
| -------------------- | --------------------------- |
| **Language**         | Python 3.10+                |
| **Database**         | MongoDB Atlas               |
| **Modeling**         | scikit-learn, pandas, NumPy |
| **Version Control**  | DVC                         |
| **Containerization** | Docker                      |
| **Cloud Services**   | AWS S3, EC2, ECR            |
| **CI/CD**            | GitHub Actions              |
| **Logging**          | Custom Python Logger        |
| **Environment**      | Conda, Pyproject.toml       |

---
### Results.
- Successfully automated vehicle claim prediction pipeline.
-  Model pushed & retrieved dynamically from AWS S3.
- Full CI/CD integration using Docker + GitHub Actions.
- Modular architecture enabling scalable MLOps design.
- ML models giving 85% accuracy.

---
### Future Enhancements
- Integrate MLflow for model versioning
- Add Prometheus/Grafana monitoring
- Automate retraining on new data
- Convert API into AWS Lambda microservice

---

### Author
@Aditya Akuskar
- [Linkedin](https://www.linkedin.com/in/aditya-a-27b43533a/)





