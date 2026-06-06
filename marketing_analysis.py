
# MARKETING FUNNEL & CONVERSION PERFORMANCE ANALYSIS
# Complete Internship Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: CREATE A REALISTIC MARKETING DATASET
np.random.seed(42)
n = 5000

channels = ["Google Ads", "Facebook Ads", "Instagram", "Email", "Organic Search"]

channel_probs = [0.25, 0.25, 0.20, 0.15, 0.15]

df = pd.DataFrame({"User_ID": range(1, n + 1), "Channel": np.random.choice(channels, size=n, p=channel_probs)})

# Visitor Stage
df["Visitor"] = 1

#lead probabilities by channel
lead_rates = {"Google Ads": 0.22,
    "Facebook Ads": 0.18,
    "Instagram": 0.15,
    "Email": 0.35,
    "Organic Search": 0.25}

df["Lead"] = df["Channel"].apply(lambda x: np.random.binomial(1, lead_rates[x]))

# Qualified Lead probabilities
qualified_rates = {
    "Google Ads": 0.55,
    "Facebook Ads": 0.45,
    "Instagram": 0.40,
    "Email": 0.70,
    "Organic Search": 0.60}

df["Qualified_Lead"] = df.apply(
    lambda row: (np.random.binomial(1, qualified_rates[row["Channel"]])
        if row["Lead"] == 1
        else 0), axis=1)

# Customer probabilities
customer_rates = {"Google Ads": 0.25,
    "Facebook Ads": 0.20,
    "Instagram": 0.18,
    "Email": 0.40,
    "Organic Search": 0.30}

df["Customer"] = df.apply(lambda row: (np.random.binomial(1, customer_rates[row["Channel"]])
        if row["Qualified_Lead"] == 1
        else 0), axis=1)

# Create random dates
dates = pd.date_range(start="2025-01-01", end="2025-12-31")

df["Date"] = np.random.choice(dates, size=n)

# Save dataset
df.to_csv("marketing_funnel_dataset.csv", index=False)

print("Dataset created successfully.")
print(df.head())

# STEP 2: DATA CLEANING
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

df = df.drop_duplicates()

# STEP 3: FUNNEL METRICS
visitors = len(df)
leads = df["Lead"].sum()
qualified = df["Qualified_Lead"].sum()
customers = df["Customer"].sum()

visitor_to_lead = (leads / visitors) * 100
lead_to_qualified = (qualified / leads) * 100
qualified_to_customer = (customers / qualified) * 100
overall_conversion = (customers / visitors) * 100

print("\n==============================")
print("FUNNEL METRICS")
print("==============================")

print(f"Visitors: {visitors}")
print(f"Leads: {leads}")
print(f"Qualified Leads: {qualified}")
print(f"Customers: {customers}")

print(f"\nVisitor -> Lead: {visitor_to_lead:.2f}%")
print(f"Lead -> Qualified: {lead_to_qualified:.2f}%")
print(f"Qualified -> Customer: {qualified_to_customer:.2f}%")
print(f"Overall Conversion: {overall_conversion:.2f}%")

# STEP 4: FUNNEL TABLE
funnel = pd.DataFrame({
    "Stage": ["Visitors", "Leads", "Qualified Leads", "Customers"],
    "Count": [visitors, leads, qualified, customers]})

funnel["Drop_Off"] = (funnel["Count"].shift(1) - funnel["Count"])

print("\nFunnel Table")
print(funnel)


# STEP 5: FUNNEL VISUALIZATION
plt.figure(figsize=(8, 5))
sns.barplot(data=funnel, x="Stage", y="Count")

plt.title("Marketing Funnel")
plt.tight_layout()
plt.show()

# STEP 6: CHANNEL PERFORMANCE

channel_summary = df.groupby("Channel").agg(
    Visitors=("Visitor", "sum"),
    Leads=("Lead", "sum"),
    Qualified=("Qualified_Lead", "sum"),
    Customers=("Customer", "sum"))

channel_summary["Lead_Rate_%"] = (channel_summary["Leads"] / channel_summary["Visitors"]) * 100

channel_summary["Customer_Rate_%"] = (channel_summary["Customers"] / channel_summary["Visitors"]) * 100

print("\nChannel Performance")
print(channel_summary)

# STEP 7: CHANNEL VISUALIZATION
plt.figure(figsize=(10, 6))
channel_summary["Customer_Rate_%"].sort_values(ascending=False).plot(kind="bar")

plt.title("Customer Conversion Rate by Channel")
plt.ylabel("Conversion Rate (%)")
plt.tight_layout()
plt.show()

# STEP 8: MONTHLY CONVERSIONS

df["Date"] = pd.to_datetime(df["Date"])
monthly_customers = df.groupby(pd.Grouper(key="Date", freq="M"))["Customer"].sum()

plt.figure(figsize=(10, 5))

monthly_customers.plot()
plt.title("Monthly Customer Conversions")
plt.ylabel("Customers")
plt.grid(True)
plt.tight_layout()
plt.show()

# STEP 9: DROP-OFF ANALYSIS

drop_visitor_lead = visitors - leads
drop_lead_qualified = leads - qualified
drop_qualified_customer = qualified - customers

print("\n==============================")
print("DROP-OFF ANALYSIS")
print("==============================")

print(f"Visitor -> Lead Drop-off: " f"{drop_visitor_lead}")
print(f"Lead -> Qualified Drop-off: " f"{drop_lead_qualified}")
print(f"Qualified -> Customer Drop-off: " f"{drop_qualified_customer}")

# STEP 10: BUSINESS INSIGHTS
print("\n==============================")
print("BUSINESS INSIGHTS")

largest_drop = max(drop_visitor_lead, drop_lead_qualified, drop_qualified_customer)

if largest_drop == drop_visitor_lead:
    print("Largest drop-off occurs between " "Visitors and Leads.")
elif largest_drop == drop_lead_qualified:
    print("Largest drop-off occurs between " "Leads and Qualified Leads.")
else:
    print("Largest drop-off occurs between " "Qualified Leads and Customers.")

best_channel = channel_summary["Customer_Rate_%"].idxmax()

print(f"Best Performing Channel: " f"{best_channel}")
print("\nRecommendations:")

print("1. Improve landing pages to increase " "Visitor-to-Lead conversion.")
print("2. Invest more budget into the " "best-performing channel.")
print("3. Use email nurturing campaigns " "to convert more leads.")
print("4. Run A/B tests on forms, ads, " "and landing pages.")
print("\nProject Completed Successfully!")