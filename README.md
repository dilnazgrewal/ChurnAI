# 📊 Customer Churn Prediction System

An end-to-end Machine Learning project that predicts whether a telecom customer is likely to churn. The system leverages a **Threshold-Optimized Logistic Regression** model along with **SHAP (SHapley Additive exPlanations)** to provide transparent and interpretable predictions. A Streamlit-based web application allows users to input customer details and receive churn predictions with business-friendly explanations and retention recommendations.

---

## 🚀 Features

- Predict customer churn probability
- Threshold-optimized Logistic Regression model
- Automated preprocessing using Scikit-learn Pipeline
- Explainable AI with SHAP
- Customer-specific churn risk analysis
- Business-friendly retention recommendations
- Streamlit-based interactive web application
- Model serialization using Joblib

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Machine Learning
- Scikit-learn
- Logistic Regression
- SHAP

### Data Processing
- Pandas
- NumPy

### Data Visualization
- Matplotlib

### Backend
- Flask

### Model Deployment
- Joblib

### Development Tools
- Jupyter Notebook
- VS Code
- Git & GitHub

---

## 📂 Project Structure

```
customer-churn-prediction/
│
├── 📂 model                 # Trained ML pipeline & serialized artifacts
├── 📂 notebooks             # EDA, preprocessing & model development
├── 📂 pages                 # Streamlit application pages
├── 📂 utils                 # Prediction, SHAP & helper modules
│
├── 📄 app.py                # Streamlit entry point
├── 📄 theme.py              # Custom UI theme
├── 📄 config.toml           # Streamlit configuration
├── 📄 requirements.txt      # Project dependencies
├── 📄 README.md             # Project documentation
├── 📄 .gitignore            # Git ignore rules
└── 📄 .env                  # Environment variables (excluded from Git)
```

---

## 📊 Dataset

The project uses the **IBM Telco Customer Churn Dataset**, containing customer demographics, subscribed services, billing information, and churn status.

**Target Variable**
- Churn Label (Yes / No)

---

## 🔄 Project Workflow

```
Customer Data
      │
      ▼
Data Cleaning
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Feature Engineering
      │
      ▼
Train-Test Split
      │
      ▼
Model Training
      │
      ▼
Hyperparameter Tuning
      │
      ▼
Threshold Optimization
      │
      ▼
Pipeline Creation
      │
      ▼
SHAP Explainability
      │
      ▼
Streamlit Deployment
```

---

## 🤖 Models Evaluated

The following machine learning models were trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

Each model was assessed using:

- Baseline Performance
- Hyperparameter Tuning
- SMOTE
- SMOTEENN
- Threshold Optimization

---

## 🏆 Final Model

**Threshold-Optimized Logistic Regression**

### Performance

| Metric | Score |
|---------|-------|
| Accuracy | **80.03%** |
| Precision | **61.77%** |
| Recall | **65.24%** |
| F1-Score | **63.46%** |
| ROC-AUC | **84.43%** |

### Why Logistic Regression?

Multiple machine learning models, including Logistic Regression, Decision Tree, Random Forest, and XGBoost, were evaluated using baseline training, hyperparameter tuning, resampling techniques (SMOTE/SMOTEENN), and threshold optimization.

Although Threshold-Optimized XGBoost achieved a slightly higher F1-score and ROC-AUC, the improvement was marginal. Threshold-Optimized Logistic Regression delivered comparable predictive performance while offering superior interpretability, computational efficiency, and seamless integration with SHAP for explainable AI. These advantages made it the preferred choice for deployment.

---

## 📈 Explainable AI

The application uses **SHAP (SHapley Additive exPlanations)** to explain every prediction by highlighting:

- Features increasing churn risk
- Features reducing churn risk
- Individual feature contributions
- Business-friendly interpretation
- Personalized retention recommendations

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/customer-churn-prediction.git
```

Navigate to the project directory:

```bash
cd customer-churn-prediction
```

Create a virtual environment (Optional):

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📌 Future Improvements

- Batch customer prediction
- Customer retention dashboard
- REST API support
- Cloud deployment
- Model monitoring and retraining
- Authentication system

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

## 👨‍💻 Author

**Dilnaz Grewal**

B.Tech Computer Science & Engineering  
Guru Nanak Dev Engineering College

---

⭐ If you found this project useful, consider giving it a star!