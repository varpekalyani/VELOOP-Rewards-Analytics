# 🎁 VELOOP Rewards Analytics Dashboard

### 📊 Turning User Data into Actionable Insights

An interactive data analytics dashboard built with **Python, Streamlit, Pandas, and Plotly** to explore user activity, onboarding progress, account status, data quality, and analytics readiness for a rewards platform.

The project focuses on transforming user data into meaningful insights while identifying gaps in rewards, wallet, withdrawal, and event-tracking data.

---

## 🚀 Project Overview

The VELOOP Rewards Analytics Dashboard provides an interactive way to understand user data and assess the availability of information needed for rewards analytics.

Users can explore registration trends, account status, onboarding progress, verification status, and data quality through interactive visualizations and filters.

The dashboard also highlights areas where additional transaction and event data would be required for complete rewards analytics.

> **Important:** The available user dataset is used for analysis. Rewards, wallet, withdrawal, and referral transaction insights remain subject to the availability and validation of their underlying data.

---

## ✨ Key Features

📌 **Executive Overview**
- View key user statistics.
- Explore account and onboarding status.
- Analyze registration trends.
- Review high-level user insights.

👥 **User Analytics**
- Explore user registration patterns.
- Analyze onboarding completion.
- Examine account and verification status.
- Filter data by available location and platform fields.

🔍 **Interactive Data Explorer**
- Preview available user records.
- Apply interactive filters.
- Explore selected data fields.
- Download filtered data when supported.

🧹 **Data Quality Analysis**
- Identify missing values.
- Review data completeness.
- Inspect dataset structure.
- Highlight potential data quality issues.

💰 **Rewards & Wallet Readiness**
- Review analytics requirements for rewards and wallet features.
- Identify missing transaction data.
- Understand the information required for future KPI tracking.
- Separate available data from proposed analytics requirements.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard development |
| Pandas | Data processing and analysis |
| Plotly | Interactive charts and visualizations |
| CSV / Excel | Data storage and source data |

---

## 📂 Project Structure

```text
21_dashboard_App/
│
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    └── users.csv