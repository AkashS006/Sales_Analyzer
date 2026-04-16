# Sales Analyzer
## Author: AKASH S

## 📌 Table of Contents

* 📖 Project Overview
* 🎯 Objectives
* 🗂️ Project Structure
* ⚙️ Technology Stack
* 🖥️ Python Desktop UI
* 📊 R Markdown Report
* 🗄️ Dataset — Why We Built Our Own
* 🔧 How the Dataset Was Built
* ✅ Dataset Quality
* 📈 Key Business Insights
* 🚀 How to Run
* 📦 Requirements
* 📁 Output Files
* 🔮 Future Scope

---

## 📖 Project Overview

The **Sales Data Analysis System** is a complete, production-style data analytics project built from scratch. It covers every stage of the data lifecycle:

📦 Data Generation → 🖥️ Desktop UI → 🧹 Data Cleaning
↓
📊 EDA & Visualization → 👤 Customer Profiling → 📄 PDF Report

The project is split into two major layers:

| Layer             | Technology               | Purpose              |
| ----------------- | ------------------------ | -------------------- |
| Application Layer | Python + PyQt5 + SQLite  | Desktop UI           |
| Analytics Layer   | R + R Markdown + ggplot2 | Analysis & reporting |

---

## 🎯 Objectives

* Build custom dataset using Python
* Create desktop UI using PyQt5
* Perform full data cleaning in R
* Conduct EDA with 15+ charts
* Build RFM profiles
* Generate PDF report

---

## 🗂️ Project Structure

Sales_Analyzer/
│
├── Data/
├── Output/
├── Processed Data/
├── app.py
├── main_window.py
├── datagenerator.py
├── Sales_Analysis_Report.Rmd
├── Sales_Analysis_Report.pdf
└── requirements.txt

---

## ⚙️ Technology Stack

### Python

* PyQt5
* SQLite3
* Pandas
* NumPy
* Faker
* Matplotlib

### R

* tidyverse
* ggplot2
* dplyr
* lubridate
* ggcorrplot
* janitor

---

## 🖥️ Python Desktop UI

Modules:

* Home Dashboard
* Sales Entry
* Employee Management
* Stock Management
* User Management

---

## 📊 R Markdown Report

Includes:

* Dataset overview
* Statistical summary
* Data cleaning
* Feature engineering
* RFM segmentation
* 15 visualizations
* Business insights

---

## 🗄️ Dataset

* 9,140 transactions
* 300 customers
* 105 products
* 10 cities
* Revenue: ₹22.9 Crore

---

## 🔧 Dataset Highlights

* Realistic behavior simulation
* Seasonal trends
* Payment distribution
* Customer segmentation

---

## ✅ Dataset Quality

✔ No missing values
✔ No duplicates
✔ Valid ranges
✔ All checks passed

---

## 📈 Key Insights

* Electronics → 68% revenue
* Mumbai → Top city
* Monsoon → Best season
* VIP customers → Major revenue drivers

---

## 🚀 How to Run

### Python App

git clone [https://github.com/AkashS006/Sales_Analyzer.git](https://github.com/AkashS006/Sales_Analyzer.git)
cd Sales_Analyzer
pip install -r requirements.txt
python app.py

---

### R Report

Open Rmd → Click Knit → Generate PDF

---

### Dataset

python datagenerator.py

---

## 📦 Requirements

Python:

* PyQt5
* pandas
* numpy
* faker

R:

* tidyverse
* ggplot2
* dplyr

---

## 📁 Output Files

* sales.csv
* clean_sales_data.csv
* customer_profile.csv
* plots
* PDF report

---

## 🔮 Future Scope

* Machine Learning models
* Streamlit dashboard
* POS integration
* Forecasting
* Web deployment

---

## 📬 Connect

GitHub: [https://github.com/AkashS006](https://github.com/AkashS006)

---

> *"Data is the new oil — but only if you know how to refine it."*
