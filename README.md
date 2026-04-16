Here is the complete updated README.md — copy everything between the two lines and paste directly into GitHub:

---

```markdown
<div align="center">

# 🛒 Sales Data Analysis System
### End-to-End Data Analytics Project with Python UI & R Report

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-4.5.2-276DC3?style=for-the-badge&logo=r&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop_UI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![RMarkdown](https://img.shields.io/badge/R_Markdown-PDF_Report-blue?style=for-the-badge&logo=markdown&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-2ECC71?style=for-the-badge)

<br/>

> **A complete end-to-end sales analytics pipeline —**  
> from custom dataset generation to desktop UI to automated PDF report.

<br/>

**Author:** Akash S &nbsp;|&nbsp; **Roll No:** 2026EMAI10065 &nbsp;|&nbsp;
**Domain:** Data Analytics

---

</div>

<br/>

## 📌 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🎯 Objectives](#-objectives)
- [🗂️ Project Structure](#️-project-structure)
- [⚙️ Technology Stack](#️-technology-stack)
- [🖥️ Python Desktop UI](#️-python-desktop-ui)
- [📊 R Markdown Report](#-r-markdown-report)
- [🗄️ Dataset — Why We Built Our Own](#️-dataset--why-we-built-our-own)
- [🔧 How the Dataset Was Built](#-how-the-dataset-was-built)
- [✅ Dataset Quality](#-dataset-quality)
- [📈 Key Business Insights](#-key-business-insights)
- [🚀 How to Run](#-how-to-run)
- [📦 Requirements](#-requirements)
- [📁 Output Files](#-output-files)
- [🔮 Future Scope](#-future-scope)

---

<br/>

## 📖 Project Overview

The **Sales Data Analysis System** is a complete, production-style data analytics
project built from scratch. It covers every stage of the data lifecycle:

```
📦 Data Generation  →  🖥️ Desktop UI  →  🧹 Data Cleaning
        ↓
📊 EDA & Visualization  →  👤 Customer Profiling  →  📄 PDF Report
```

The project is split into two major layers:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Application Layer** | Python + PyQt5 + SQLite | Desktop UI for data entry & management |
| **Analytics Layer** | R + R Markdown + ggplot2 | Data cleaning, EDA, RFM analysis, PDF report |

### 📦 Dataset at a Glance

| Metric | Value |
|--------|-------|
| Total Transactions | 9,140 rows |
| Unique Customers | 300 |
| Unique Products | 105 |
| Product Categories | 10 |
| Cities Covered | 10 Indian cities |
| Date Range | Jan 2023 — Mar 2024 |
| Total Revenue | Rs 22.9 Crore |
| Quality Checks Passed | 12 of 12 ✅ |

---

<br/>

## 🎯 Objectives

- ✅ Build a **realistic custom sales dataset** from scratch using Python
- ✅ Develop a **Python desktop application** for data entry and management
- ✅ Perform complete **data cleaning and feature engineering** in R
- ✅ Conduct deep **Exploratory Data Analysis** with 15+ visualizations
- ✅ Build **RFM customer profiles** and predict next purchase dates
- ✅ Generate a professional **automated PDF report** using R Markdown

---

<br/>

## 🗂️ Project Structure

```
📁 Sales_Analyzer/
│
├── 📁 Data/                          ← Raw source data
│   ├── 📊 sales.csv                  ← Main generated dataset (9140 rows)
│   ├── 📊 employee.csv               ← Employee data
│   ├── 📊 stocks.csv                 ← Stock inventory data
│   └── 📊 user.csv                   ← User/Customer data
│
├── 📁 Output/                        ← All analysis outputs
│   ├── 📁 Data/                      ← Processed CSV files
│   │   ├── 📊 clean_sales_data.csv   ← Cleaned dataset (30 columns)
│   │   ├── 📊 customer_profile.csv   ← 300 RFM profiles
│   │   ├── 📊 monthly_trend.csv      ← Monthly revenue summary
│   │   └── 📊 category_summary.csv   ← Category-wise summary
│   │
│   ├── 📁 Plots/                     ← All 15 generated charts
│   │   ├── 🖼️ 9A_monthly_revenue_trend.png
│   │   ├── 🖼️ 9B_revenue_by_day.png
│   │   ├── 🖼️ 9C_revenue_by_quarter.png
│   │   ├── 🖼️ 9D_revenue_by_season.png
│   │   ├── 🖼️ 9E_category_revenue.png
│   │   ├── 🖼️ 9F_segment_analysis.png
│   │   ├── 🖼️ 9G_gender_age_revenue.png
│   │   ├── 🖼️ 9H_payment_channel.png
│   │   ├── 🖼️ 9I_city_revenue.png
│   │   ├── 🖼️ 9J_rfm_segments.png
│   │   ├── 🖼️ 9K_spend_distribution.png
│   │   ├── 🖼️ 9L_correlation_heatmap.png
│   │   ├── 🖼️ 9M_top10_products.png
│   │   ├── 🖼️ 9N_time_channel.png
│   │   └── 🖼️ 9O_category_payment_heatmap.png
│   │
│   └── 📁 Reports/
│       └── 📃 analysis_summary.txt
│
├── 📁 Processed Data/                ← Intermediate processed files
│   └── 📊 process_sales_data.csv
│
├── 🐍 app.py                         ← Main application entry point
├── 🐍 main_window.py                 ← Main window and navigation
├── 🐍 home.py                        ← Home dashboard page
├── 🐍 sales_entry.py                 ← Sales transaction entry
├── 🐍 add_employee.py                ← Employee management
├── 🐍 add_stocks.py                  ← Stock management
├── 🐍 add_user.py                    ← User management
├── 🐍 data_manager.py                ← SQLite database handler
├── 🐍 datagenerator.py               ← Custom dataset generator
│
├── 📝 Sales_Analysis_Report.Rmd      ← R Markdown report source
├── 📄 Sales_Analysis_Report.pdf      ← Final generated PDF report
├── 📝 Data_analysis.R                ← Standalone R analysis script
│
└── 📃 requirements.txt               ← Python dependencies
```

---

<br/>

## ⚙️ Technology Stack

### 🐍 Python Side

| Library | Version | Purpose |
|---------|---------|---------|
| PyQt5 | Latest | Desktop UI framework |
| SQLite3 | Built-in | Local database storage |
| Pandas | Latest | Data handling and export |
| Faker | Latest | Realistic data generation |
| NumPy | Latest | Random distributions |
| Matplotlib | Latest | Quick visualizations |

### 📊 R Side

| Package | Purpose |
|---------|---------|
| tidyverse | Full data ecosystem |
| ggplot2 | All visualizations |
| dplyr | Data manipulation |
| knitr + kableExtra | PDF tables |
| lubridate | Date handling |
| ggridges | Ridge plots |
| ggcorrplot | Correlation matrix |
| moments | Skewness analysis |
| janitor | Data cleaning |
| viridis + RColorBrewer | Color palettes |

---

<br/>

## 🖥️ Python Desktop UI

A full desktop application built with **PyQt5** for managing sales data
across 4 modules, all connected to a local **SQLite database**.

### 🏠 Home Page — `home.py`
> Central navigation hub. First screen on launch.
> Contains buttons to navigate to all 4 modules.

### 🛒 Sales Entry — `sales_entry.py`
> Add new sales transactions with full field entry.
> Auto-calculates Total Spend from Quantity × Unit Price.

```
Fields: Customer Name | Product | Category | Quantity
        Unit Price | Payment Method | Channel | City | Date
```

### 👷 Employee Management — `add_employee.py`
> Add and view employee records.

```
Fields: Name | Role | Department | City | Mobile | Join Date
```

### 📦 Stock Management — `add_stocks.py`
> Track product inventory levels across categories.

```
Fields: Product Name | Category | Stock Quantity | Unit Price
```

### 👤 User Management — `add_user.py`
> Manage customer and user profiles.

```
Fields: Name | Age | Gender | City | Segment | Mobile Number
```

### 🗄️ Data Manager — `data_manager.py`
> Handles all SQLite read/write operations.
> Single source of truth for all database interactions.

---

<br/>

## 📊 R Markdown Report

The **automated PDF report** is generated using R Markdown and covers:

| Section | Content |
|---------|---------|
| Dataset Overview | Row count, column info, data types |
| Statistical Summary | Min, Max, Mean, Median, SD, Skewness |
| Categorical Distributions | All 6 categorical columns analyzed |
| Data Quality Report | 12 validation checks, outlier detection |
| Data Cleaning | 9 cleaning steps applied |
| Feature Engineering | 15 new columns created |
| Customer Profiling | 300 RFM profiles built |
| EDA Visualizations | 15 charts generated |
| Business Insights | Revenue, customer, channel analysis |
| Recommendations | 8 strategic recommendations |

### 📐 15 New Features Engineered

```
year          month_num      month_name     day
hour          day_of_week    quarter        is_weekend
is_month_end  season         time_of_day    age_group
spend_tier    log_unit_price log_total_spend
```

### 👤 RFM Customer Segments Built

| Segment | Description |
|---------|-------------|
| 🏆 Champions | Highest RFM score — buy often, spend most |
| 💙 Loyal Customers | Frequent buyers with strong scores |
| 🌱 Potential Loyalists | Recent buyers with growth potential |
| 🆕 New Customers | Recently acquired customers |
| ⚠️ At Risk | Used to buy frequently but slowing down |
| ❌ Lost | Have not bought in a long time |

---

<br/>

## 🗄️ Dataset — Why We Built Our Own

Instead of using a ready-made dataset from Kaggle or any online source,
we built our own from scratch. Here is why:

| ❌ Problem with Online Datasets | ✅ Our Custom Dataset |
|-------------------------------|----------------------|
| Already cleaned — no real challenge | Controlled noise for realistic cleaning |
| Generic — not India-specific | 10 real Indian cities and UPI payments |
| Fixed size — cannot scale | Scalable to any number of rows |
| Missing columns we needed | Exactly the 15 columns we designed |
| Overused in academic projects | 100% unique and original |
| No control over distributions | Full control over every distribution |
| Cannot simulate behavior patterns | Seasonal and loyalty patterns embedded |

---

<br/>

## 🔧 How the Dataset Was Built

The dataset was generated using **`datagenerator.py`** following
a 10-step logic pipeline:

### Step 1 — 👥 Customer Pool Creation
```
300 unique customer IDs created: C001 to C300
Each customer assigned fixed attributes:
Name, Age, Gender, City, Segment, Mobile Number

Segment weights:
  VIP           → 15%
  Premium       → 25%
  Regular       → 40%
  New Customer  → 20%
```

### Step 2 — 🔁 Transaction Frequency
```
Each customer assigned a purchase frequency:
  Weekly Buyer      → VIP customers
  Bi-Weekly Buyer   → Premium customers
  Monthly Buyer     → Regular customers
  Occasional Buyer  → Mixed
  Rare Buyer        → New customers (1-3 purchases)

Result: 9,140 total transactions generated
```

### Step 3 — 📅 Date & Time Logic
```
Date range: January 2023 to March 2024
  → Weekends boosted by 30% higher probability
  → Month-end (25th-31st) boosted by 20%
    to simulate salary-day spending
  → Monsoon (June-Sept) has peak volume
  → Hours: 8 AM to 11 PM only
```

### Step 4 — 🛍️ Product & Category Assignment
```
10 categories | 105 unique products
Each customer has a favorite category (60% probability)
Remaining 40% from random other categories

Price ranges by category:
  Electronics  → Rs 5,000   to Rs 1,50,000
  Groceries    → Rs 50      to Rs 2,000
  Clothing     → Rs 500     to Rs 8,000
  Furniture    → Rs 3,000   to Rs 50,000
```

### Step 5 — 💰 Price Distribution Logic
```
Each product has a fixed base price range
Price varies ±10% to simulate market fluctuation
Hard rule enforced: Total Spend = Quantity × Unit Price
```

### Step 6 — 💳 Payment Method Weights
```
Assigned based on Indian payment behavior:
  UPI          → 27%   (most popular in India)
  Credit Card  → 26%
  Debit Card   → 20%
  Cash         → 10%
  Wallet       → 9%
  Net Banking  → 8%

Online channel  → prefers UPI
In-Store        → prefers Cash and Debit Card
```

### Step 7 — 📱 Channel Distribution
```
Online     → 37%
Mobile App → 26%
In-Store   → 25%
Phone      → 12%

Age-based logic:
  18-35 → Online and Mobile App preferred
  46+   → In-Store and Phone preferred
```

### Step 8 — 🏙️ City Distribution
```
Mumbai     → 15%   Delhi      → 14%
Bangalore  → 14%   Hyderabad  → 11%
Chennai    → 10%   Kolkata    → 10%
Ahmedabad  → 9%    Jaipur     → 8%
Surat      → 5%    Pune       → 4%
Based on population and retail market size
```

### Step 9 — 🔍 Noise & Validation
```
Controlled noise added:
  → Some customers have long purchase gaps
    to simulate churn behavior
  → A few products appear rarely
    to simulate seasonal items

Validations enforced:
  → Total Spend always equals Qty × Price
  → Mobile numbers always 10 digits
  → Dates always within valid range
  → Age always between 18 and 65
  → No null or empty values
```

### Step 10 — 📤 Final Export
```
Total Rows       : 9,140
Total Columns    : 15
Unique Customers : 300
Unique Products  : 105
Date Range       : Jan 2023 to Mar 2024
File Size        : ~1.2 MB
Format           : CSV — UTF-8 encoded
Output File      : Sales_Analyzer/Data/sales.csv
```

---

<br/>

## ✅ Dataset Quality

All **12 validation checks passed** with zero issues:

| # | Check | Issues Found | Result |
|---|-------|-------------|--------|
| 1 | Missing Values | 0 | ✅ PASS |
| 2 | Full Duplicates | 0 | ✅ PASS |
| 3 | Partial Duplicates | 0 | ✅ PASS |
| 4 | Age Range 18-100 | 0 | ✅ PASS |
| 5 | Quantity > 0 | 0 | ✅ PASS |
| 6 | Unit Price > 0 | 0 | ✅ PASS |
| 7 | Total Spend > 0 | 0 | ✅ PASS |
| 8 | Future Dates | 0 | ✅ PASS |
| 9 | Pre-2020 Dates | 0 | ✅ PASS |
| 10 | Mobile 10 Digits | 0 | ✅ PASS |
| 11 | Spend = Qty × Price | 0 | ✅ PASS |
| 12 | Valid Category Values | 0 | ✅ PASS |

---

<br/>

## 📈 Key Business Insights

### 💰 Revenue Highlights
```
Total Revenue       →  Rs 22.9 Crore
Avg Transaction     →  Rs 25,057
Top Category        →  Electronics (68% of revenue)
Top City            →  Mumbai (15% of revenue)
Best Season         →  Monsoon
Best Quarter        →  Q3
```

### 👥 Customer Highlights
```
VIP Segment         →  49.5% of customers, 54% of revenue
Champions RFM       →  Highest value customers
Lost Customers      →  85 need immediate re-engagement
Weekly Buyers       →  Need loyalty reward program
```

### 💡 Strategic Recommendations
```
1. Re-engage 85 Lost customers with personalised offers
2. Diversify revenue beyond Electronics category
3. Grow Online + Mobile App channels (62.5% combined)
4. Onboard New Customers within first 30 days
5. Reward Weekly and Bi-Weekly buyers with perks
6. Amplify Monsoon season promotions
7. Offer UPI cashback and Credit Card EMI options
8. Target Chennai and Pune with focused campaigns
```

---

<br/>

## 🚀 How to Run

### 🐍 Run the Python Desktop UI

**Step 1 — Clone the repository**
```bash
git clone https://github.com/yourusername/Sales_Analyzer.git
cd Sales_Analyzer
```

**Step 2 — Install Python dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Launch the application**
```bash
python app.py
```

---

### 📊 Generate the R Markdown PDF Report

**Step 1 — Open RStudio**
```
Open Sales_Analyzer/Sales_Analysis_Report.Rmd in RStudio
```

**Step 2 — Install R packages**
```r
install.packages(c(
  "tidyverse", "lubridate", "ggplot2",
  "dplyr", "scales", "corrplot",
  "ggcorrplot", "skimr", "janitor",
  "gridExtra", "RColorBrewer", "viridis",
  "knitr", "reshape2", "ggridges",
  "moments", "kableExtra"
))
```

**Step 3 — Knit the report**
```
Click the Knit button  →  Select Knit to PDF
Output: Sales_Analyzer/Sales_Analysis_Report.pdf
```

---

### 🗄️ Generate the Dataset

```bash
python datagenerator.py
# Output: Sales_Analyzer/Data/sales.csv
```

---

<br/>

## 📦 Requirements

### Python — `requirements.txt`
```
PyQt5
pandas
numpy
faker
matplotlib
```

### R Packages
```r
tidyverse, lubridate, ggplot2, dplyr,
scales, corrplot, ggcorrplot, skimr,
janitor, gridExtra, RColorBrewer,
viridis, knitr, reshape2, ggridges,
moments, kableExtra
```

### System Requirements
```
Python  →  3.10 or higher
R       →  4.0 or higher
RStudio →  2022 or higher (for Knit)
TinyTeX →  For PDF generation
           Run: tinytex::install_tinytex()
OS      →  Windows 10/11 recommended
```

---

<br/>

## 📁 Output Files

| File | Location | Description |
|------|----------|-------------|
| `sales.csv` | Sales_Analyzer/Data/ | Raw generated dataset — 9140 rows |
| `clean_sales_data.csv` | Sales_Analyzer/Output/Data/ | Cleaned dataset — 30 columns |
| `customer_profile.csv` | Sales_Analyzer/Output/Data/ | 300 RFM customer profiles |
| `monthly_trend.csv` | Sales_Analyzer/Output/Data/ | 15-month revenue aggregation |
| `category_summary.csv` | Sales_Analyzer/Output/Data/ | 10-category performance summary |
| `9A to 9O .png` | Sales_Analyzer/Output/Plots/ | 15 EDA visualization charts |
| `analysis_summary.txt` | Sales_Analyzer/Output/Reports/ | Text summary of analysis |
| `Sales_Analysis_Report.pdf` | Sales_Analyzer/ | Full automated PDF report |

---

<br/>

## 🔮 Future Scope

- [ ] **Machine Learning** — Add price and demand forecasting models
- [ ] **Streamlit Dashboard** — Build a real-time interactive web dashboard
- [ ] **Live POS Integration** — Connect to a real Point of Sale system
- [ ] **Revenue Forecasting** — Predict next month revenue using ARIMA
- [ ] **Web Deployment** — Deploy as a full-stack web application
- [ ] **Email Alerts** — Auto-alert for low stock and churned customers
- [ ] **NLP Reviews** — Add customer review sentiment analysis
- [ ] **Mobile App** — Build a companion mobile application

---

<br/>

<div align="center">

## 📬 Connect

**Akash S** &nbsp;|&nbsp;

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

---

> *"Data is the new oil — but only if you know how to refine it."*

<br/>

**Made with ❤️ using Python 🐍 and R 📊**

</div>
```
