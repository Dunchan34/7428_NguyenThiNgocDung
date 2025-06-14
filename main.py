
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="ABC Manufacturing Demand Forecasting", layout="wide")

# Title and introduction
st.title("ABC Manufacturing: Demand Forecasting Dashboard")
st.markdown("""
This dashboard supports the Operations Director by providing demand forecasting based on historical sales data. 
It helps optimize inventory levels, reduce stockouts, and improve resource utilization.
""")

# Function to generate sample data (simulating ABC Manufacturing's sales data)
@st.cache_data
def load_data():
    dates = pd.date_range(start="2023-01-01", end="2025-06-01", freq="M")
    np.random.seed(42)
    sales = np.random.normal(loc=1000, scale=200, size=len(dates)) + np.linspace(0, 500, len(dates))
    data = pd.DataFrame({"Date": dates, "Sales": sales})
    data["Month"] = data["Date"].dt.month
    data["Year"] = data["Date"].dt.year
    return data

# Load data
data = load_data()

# Sidebar for user inputs
st.sidebar.header("Forecasting Parameters")
forecast_horizon = st.sidebar.slider("Select forecast horizon (months):", 1, 12, 6)
model_type = st.sidebar.selectbox("Select Model:", ["Linear Regression", "Moving Average"])

# Data preprocessing
def preprocess_data(data):
    data["Time"] = np.arange(len(data))
    return data

data = preprocess_data(data)

# Forecasting function
def forecast_demand(data, horizon, model_type):
    if model_type == "Linear Regression":
        X = data[["Time"]]
        y = data["Sales"]
        model = LinearRegression()
        model.fit(X, y)
        
        future_times = np.arange(len(data), len(data) + horizon).reshape(-1, 1)
        forecast = model.predict(future_times)
        
        future_dates = [data["Date"].iloc[-1] + timedelta(days=30 * i) for i in range(1, horizon + 1)]
        return pd.DataFrame({"Date": future_dates, "Forecasted Sales": forecast})
    
    elif model_type == "Moving Average":
        window = 3
        forecast = []
        future_dates = [data["Date"].iloc[-1] + timedelta(days=30 * i) for i in range(1, horizon + 1)]
        last_values = data["Sales"].tail(window).values
        for _ in range(horizon):
            forecast.append(np.mean(last_values))
            last_values = np.append(last_values[1:], forecast[-1])
        return pd.DataFrame({"Date": future_dates, "Forecasted Sales": forecast})

# Perform forecasting
forecast_data = forecast_demand(data, forecast_horizon, model_type)

# Visualizations
st.subheader("Historical Sales and Forecast")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data["Date"], data["Sales"], label="Historical Sales", marker="o")
ax.plot(forecast_data["Date"], forecast_data["Forecasted Sales"], label="Forecasted Sales", marker="x", linestyle="--")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# Display data tables
st.subheader("Historical Sales Data")
st.dataframe(data[["Date", "Sales"]].style.format({"Sales": "{:.2f}"}))

st.subheader("Forecasted Sales")
st.dataframe(forecast_data.style.format({"Forecasted Sales": "{:.2f}"}))

# Recommendations
st.subheader("Recommendations for Operations Director")
st.markdown("""
Based on the forecasted demand:
1. **Inventory Optimization**: Adjust inventory levels to align with forecasted sales to prevent stockouts or excess inventory.
2. **Production Planning**: Schedule production to meet the anticipated demand, ensuring efficient resource utilization.
3. **Supply Chain Coordination**: Share forecasts with suppliers to improve order fulfillment and reduce lead times.
4. **Continuous Monitoring**: Use real-time data to refine forecasts and address any discrepancies promptly.
""")

# Evaluation
st.subheader("Evaluation of Data Science Solution")
st.markdown("""
This solution leverages data science tools (Streamlit, Pandas, Scikit-learn) to provide actionable insights for ABC Manufacturing. 
The benefits include:
- **Improved Decision-Making**: Accurate forecasts enable proactive inventory and production planning.
- **Cost Efficiency**: Reduces costs associated with overstocking or stockouts.
- **Scalability**: The solution can be extended to incorporate real-time IoT data or more advanced models (e.g., ARIMA, Prophet).
- **Ethical Considerations**: Ensures data-driven decisions align with sustainable and ethical business practices.
""")
