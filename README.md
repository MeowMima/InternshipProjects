# Internship Projects — Data Analysis & Interactive Dashboards

This repository contains two data analysis and visualization projects developed as part of my internship work.

The projects focus on transforming real-world datasets into interactive dashboards, extracting meaningful insights through exploratory data analysis, statistical analysis, and data visualization.

---

## 📌 Projects

### 1. HHS Medcare — Healthcare Data Analysis

**HHS Medcare** is an interactive healthcare analytics dashboard built to analyze healthcare service data and identify operational trends, anomalies, and performance patterns.

The project combines data preprocessing, exploratory analysis, anomaly identification, visualization, and forecasting into an interactive Streamlit dashboard.

#### 🔍 Key Features

* Healthcare data exploration and preprocessing
* Interactive date-range filtering
* Multiple analysis granularities
* KPI-based healthcare performance overview
* Anomaly detection and visualization
* Interactive Plotly charts
* Trend analysis
* Forecast comparison using:

  * Naive Forecasting
  * SARIMA
  * XGBoost
* Future forecasting visualization

#### 🛠️ Technologies

`Python` `Pandas` `NumPy` `Plotly` `Streamlit`

#### 📂 Project Structure

```text
HHS_MedcareProj/
├── data/
│   ├── Cleaned_HHS_Care_Dataset.csv
│   └── HHS_Unaccompanied_Alien_Children_Program.csv
├── notebooks/
│   ├── DataPreparation.ipynb
│   ├── EDA.ipynb
│   ├── Cleaned_HHS_Care_Dataset.csv
│   └── HHS_Unaccompanied_Alien_Children_Program.csv
├── app.py
└── requirements.txt
```

### 🌐 Live Application

**HHS Medcare Dashboard:**
https://internshipprojects-hhsmedcare.streamlit.app/
---

## 2. Smart Factory Analysis — Network Performance Analytics

**Smart Factory Analysis** is an interactive data analytics dashboard designed to analyze network performance and derive statistical insights from industrial/network-related datasets.

The project focuses on exploratory data analysis, interactive visualization, KPI analysis, and statistical testing to understand network performance across different parameters.

#### 🔍 Key Features

* Interactive dataset filtering
* Network performance analysis
* KPI calculation
* Latency and throughput analysis
* Interactive Plotly visualizations
* Comparative performance analysis
* ANOVA statistical testing
* Eta-squared effect size analysis
* Automated analytical insights

#### 🛠️ Technologies

`Python` `Pandas` `Plotly` `SciPy` `Streamlit`

#### 📂 Project Structure

```text
SmartFactoryAnalysis/
├── data/
│   ├── 6GNetworkAnalysis.csv
│   └── Thales_Group_Manufacturing.csv
├── DatasetAnalysis.ipynb
├── app.py
└── requirements.txt
```

### 🌐 Live Application

**Smart Factory Analysis Dashboard:**
https://internshipprojects-smartfactoryanalysis.streamlit.app/
---

# 📊 Skills Demonstrated

Through these projects, I worked with:

* Python for data analysis
* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Pandas & NumPy
* Statistical analysis
* ANOVA
* Effect size analysis
* Data visualization with Plotly
* Interactive dashboard development with Streamlit
* Forecasting and trend analysis
* Jupyter Notebook
* Git & GitHub
* Deployment of data applications

---

# 🗂️ Repository Structure

```text
Internship/
│
├── HHS_MedcareProj/
│   ├── data/
│   ├── notebooks/
│   ├── app.py
│   └── requirements.txt
│
├── SmartFactoryAnalysis/
│   ├── data/
│   ├── DatasetAnalysis.ipynb
│   ├── app.py
│   └── requirements.txt
│
└── .gitignore
```

---

# 🚀 Running the Projects Locally

### Prerequisites

* Python 3.x
* pip
* Git

### HHS Medcare

```bash
cd HHS_MedcareProj
pip install -r requirements.txt
streamlit run app.py
```

### Smart Factory Analysis

```bash
cd SmartFactoryAnalysis
pip install -r requirements.txt
streamlit run app.py
```

---

# 👩‍💻 Author

**Mimansa Gupta**

B.Tech — Computer Science & Engineering

Interested in **AI/ML, Data Analytics, Software Development, and intelligent technology solutions.**

---

⭐ If you find these projects interesting, feel free to explore the notebooks and interactive dashboards.
