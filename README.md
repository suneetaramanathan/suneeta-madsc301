# 🌍 Global Air Quality Intelligence Pipeline

This project is developed as part of the MADSC301 – Business Intelligence course to demonstrate a full-stack ETL pipeline integrating multiple data sources, performing intelligent analysis, storing data in SQL and NoSQL databases, visualising insights, and containerising the solution for scheduled automation.

---

## 📌 Project Objectives

- Automate the end-to-end ETL process for global air quality data.
- Use both a real-time public API and a historical open dataset.
- Clean, transform, and store the data in relational and document-based databases.
- Perform meaningful analysis and visualisation to uncover pollution trends.
- Implement a simple machine learning model to predict PM2.5 concentration.
- Schedule the pipeline using a cron-based orchestrator inside Docker.

---

## 🗃️ Data Sources

1. **Public API (Real-Time)**  
   - Source: [AirVisual API](https://www.iqair.com/air-pollution-data-api)  
   - Example: Live air quality data for Los Angeles.

2. **Open Dataset (Historical)**  
   - Source: [Kaggle - Global Air Quality Dataset](https://www.kaggle.com/datasets/waqi786/global-air-quality-dataset)  
   - Format: CSV with 10,000 records of air quality metrics across major cities.

---

## 🔧 Technologies Used

| Layer                     | Tools / Libraries                                |
|---------------------------|--------------------------------------------------|
| Programming Language      | Python (v3.10)                                   |
| Data Handling             | Pandas, NumPy                                    |
| Visualisation             | Matplotlib, Seaborn                              |
| Machine Learning          | Scikit-learn (Linear Regression)                 |
| SQL Storage               | PostgreSQL (via SQLAlchemy)                      |
| NoSQL Storage             | MongoDB Atlas (via PyMongo)                      |
| Containerisation          | Docker                                           |
| Workflow Orchestration    | Cron (via crontab inside Docker container)       |
| Notebook Environment      | Jupyter Notebook                                 |

---

## 🧪 Pipeline Components

### ✅ 1. Data Collection

- Real-time data collected using AirVisual API.
- Historical data loaded from a pre-cleaned CSV file (Kaggle).

### ✅ 2. Data Cleaning & Preparation

- Removed nulls and standardised formats.
- Normalised columns, renamed headers.
- Ensured all datetime formats and location data were standardised.

### ✅ 3. Data Storage

- Cleaned data saved to:
  - PostgreSQL (`historical_air_quality`, `live_air_quality`)
  - MongoDB (`air_quality_db` collections)
- CSVs saved to `/data/processed/` for archival.

### ✅ 4. Data Analysis & Visualisation

- PM2.5 trends by city and country.
- Time series patterns.
- Correlation heatmaps between pollutants and weather features.
- Pollution composition charts.
- Real-time AQI bar plots.

### ✅ 5. Machine Learning

- Simple linear regression model to predict PM2.5 based on:
  - Temperature
  - Humidity
  - Wind Speed
- Model performance evaluated using MSE and R².

### ✅ 6. Workflow Orchestration

- The entire ETL pipeline is automated using a **cron job** inside Docker.
- Scheduled to run **daily at 9:00 AM**.
- `etl_pipeline.py` consolidates API + CSV data, processes, stores, and saves output.

---

## 📂 Project Structure

Suneeta_MADSC301/
├── etl_pipeline.py # Core ETL process (Python script)
├── suneeta-madsc301-code-file.ipynb # Jupyter Notebook with analysis & ML
├── requirements.txt # All Python dependencies
├── Dockerfile # Docker container definition
├── crontab.txt # Cron schedule for automation
├── global_air_quality_data_10000.csv # Input dataset from Kaggle
└── /data/processed/ # Auto-generated CSV outputs


---

## 🐳 Running via Docker

### Build the Docker Image:

docker build -t suneeta-madsc301-code-file .


Run the Container:

docker run -p 8888:8888 suneeta-madsc301-code-file

Access Jupyter Notebook:
Open http://127.0.0.1:8888 in your browser (token shown in terminal).

🧾 Requirements
Install all dependencies using:

pip install -r requirements.txt

📅 Cron Schedule
The following cron job runs the ETL every day at 9:00 AM inside the Docker container:

0 9 * * * python /app/etl_pipeline.py >> /var/log/cron.log 2>&1


👤 Author
Suneeta
MADSC301 Business Intelligence | May 2025