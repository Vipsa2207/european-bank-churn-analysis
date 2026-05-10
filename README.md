🏦 European Bank — Churn Intelligence Dashboard
An interactive data analytics web application built with Streamlit and Seaborn, analysing customer churn behaviour across 10,000 European bank customers.

🔗 Live Demo
👉 Click here to view the live app (replace with your deployment link)

📌 Project Overview
This project analyses customer churn patterns in a European bank dataset using exploratory data analysis (EDA), customer segmentation, and interactive visualisations. The goal is to identify high-risk customer segments and provide actionable retention insights.

📊 Key Features

Interactive Filters — Filter by Geography, Gender, Age Group, and Credit Band
6 KPI Cards — Real-time metrics including Churn Rate, Retention Rate, Revenue at Risk
Churn Overview — Distribution analysis and product-based churn rates
Geographic Analysis — Country-level churn heatmaps and comparisons
Demographics — Age group, gender, and tenure-based churn breakdown
High-Value Customer Explorer — Identify and analyse premium segment churn
Key Insights Tab — Auto-generated analytical insights with risk/opportunity flags
Churn Risk Score — Composite scoring model to classify customers by risk level


🛠️ Technology Stack
ToolPurposePythonCore programming languageStreamlitWeb application frameworkSeabornStatistical data visualisationMatplotlibGraph renderingPandasData manipulation and analysisGitHubSource code hostingStreamlit Cloud / VercelLive deployment

📂 Project Structure
european-bank-churn-analysis/
│
├── app.py                        # Main Streamlit application
├── European_Bank.csv             # Dataset (10,000 customer records)
├── logo.png                      # European Central Bank logo
└── README.md                     # Project documentation

📈 Dataset Description
ColumnDescriptionCreditScoreCustomer's credit scoreGeographyCountry (France, Spain, Germany)GenderMale / FemaleAgeCustomer ageTenureYears with the bankBalanceAccount balanceNumOfProductsNumber of bank products heldHasCrCardHas credit card (0/1)IsActiveMemberActive member status (0/1)EstimatedSalaryEstimated annual salaryExitedChurned (1) or Stayed (0) — Target variable

🔍 Key Findings

Germany has the highest churn rate at 32.4%, significantly above France (16.2%) and Spain (16.7%)
Customers aged 46–60 churn at over 51% — the highest of any age group
Inactive members churn at 26.9% vs 14.3% for active members — a 12.6pp gap
Customers with 3+ products churn at over 82%, indicating product complexity issues
Female customers churn at 25.1% vs 16.5% for males
Revenue at Risk from churned customers exceeds $185 million


🚀 How to Run Locally
bash# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/european-bank-churn-analysis.git

# 2. Navigate into the folder
cd european-bank-churn-analysis

# 3. Install dependencies
pip install streamlit pandas seaborn matplotlib

# 4. Run the app
streamlit run app.py

👩‍💻 Built By
Vipsa — Web Development Intern
Built as part of internship project requirements.

📄 License
This project is for educational purposes only.
