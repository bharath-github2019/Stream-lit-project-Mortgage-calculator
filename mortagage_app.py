import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Mortgage Calculator", layout="wide")

# Title with styling
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🏡 Mortgage Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Plan your home loan payments and visualize your amortization schedule.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("Enter Loan Details")
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=5000000, step=50000)
    interest_rate = st.slider("Annual Interest Rate (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.1)
    loan_term_years = st.slider("Loan Term (Years)", min_value=1, max_value=30, value=20)
    st.markdown("Built with ❤️ using Streamlit")

# Calculate monthly payment
monthly_rate = interest_rate / 100 / 12
months = loan_term_years * 12
monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

# Show EMI
st.subheader("📊 Monthly EMI")
st.success(f"Your monthly payment will be **₹{monthly_payment:,.2f}**")

# Generate amortization schedule
schedule = []
balance = loan_amount

for month in range(1, months + 1):
    interest = balance * monthly_rate
    principal = monthly_payment - interest
    balance -= principal
    schedule.append([month, monthly_payment, principal, interest, balance if balance > 0 else 0])

columns = ["Month", "Payment", "Principal", "Interest", "Balance"]
schedule_df = pd.DataFrame(schedule, columns=columns)

# Yearly aggregation
schedule_df["Year"] = ((schedule_df["Month"] - 1) // 12) + 1
yearly_df = schedule_df.groupby("Year")[["Principal", "Interest"]].sum().reset_index()

# Layout with graphs
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Principal vs Interest Over Years")
    fig1, ax1 = plt.subplots()
    ax1.plot(yearly_df["Year"], yearly_df["Principal"], label="Principal", marker='o')
    ax1.plot(yearly_df["Year"], yearly_df["Interest"], label="Interest", marker='x')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Amount (₹)")
    ax1.set_title("Yearly Repayment Split")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    st.subheader("📉 Loan Balance Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(schedule_df["Month"], schedule_df["Balance"], color='green')
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Remaining Balance (₹)")
    ax2.set_title("Loan Balance Decline")
    ax2.grid(True)
    st.pyplot(fig2)

# Full amortization table
with st.expander("🔍 View Full Amortization Table"):
    st.dataframe(schedule_df.style.format({"Payment": "₹{:,.2f}", "Principal": "₹{:,.2f}", "Interest": "₹{:,.2f}", "Balance": "₹{:,.2f}"}))
